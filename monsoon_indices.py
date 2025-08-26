# monsoon_indices.py
# Written by Diong Jeong Yik
import xarray as xr
import pandas as pd
import datetime
from datetime import timedelta
import argparse
import os
import mia  # import plotting functions

# ------------------- UTILITY FUNCTIONS -------------------

def subtract_days_from_date(date, days):
    subtracted_date = pd.to_datetime(date) - timedelta(days=days)
    return subtracted_date.strftime("%d-%m-%Y")

def load_dataset(file=None, yyyy=None, mm=None, dd=None, cycle="00z"):
    if file:
        print(f"Loading dataset from file/URL: {file}")
        ds = xr.open_dataset(file, engine="netcdf4")
    else:
        url = f"http://nomads.ncep.noaa.gov:80/dods/gfs_0p25/gfs{yyyy}{mm}{dd}/gfs_0p25_{cycle}"
        print(f"Fetching GFS dataset: {url}")
        ds = xr.open_dataset(url, engine="netcdf4")
    return ds

def preprocess_winds(ds):
    lat_box = [0, 30]
    lon_box = [90, 160]

    u_candidates = ["ugrdprs", "u", "uwnd"]
    v_candidates = ["vgrdprs", "v", "vwnd"]

    u_var = next((var for var in u_candidates if var in ds.variables), None)
    if not u_var:
        raise KeyError(f"No u-wind variable found. Tried: {u_candidates}")

    v_var = next((var for var in v_candidates if var in ds.variables), None)
    if not v_var:
        raise KeyError(f"No v-wind variable found. Tried: {v_candidates}")

    print(f"Using u-variable: {u_var}, v-variable: {v_var}")

    dsu_region = ds[u_var].sel(lon=slice(*lon_box), lat=slice(*lat_box))
    dsv_region = ds[v_var].sel(lon=slice(*lon_box), lat=slice(*lat_box))

    levels = dsu_region.coords.get("lev", None)
    if levels is not None:
        dsu850 = dsu_region.sel(lev=850)
        dsu925 = dsu_region.sel(lev=925)
        dsv925 = dsv_region.sel(lev=925)
    else:
        dsu850 = dsu925 = dsu_region
        dsv925 = dsv_region

    u850 = dsu850.resample(time="D").mean()
    u925 = dsu925.resample(time="D").mean()
    v925 = dsv925.resample(time="D").mean()

    return u850, u925, v925

# ------------------- ARGUMENT PARSER -------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="""
Generalized Monsoon Indices Plotting Script

This script can plot SWMI1, SWMI2, NEMI, NEMO, and MESI indices from any NetCDF dataset.
You can either provide a NetCDF file or fetch GFS 0.25° data for a specific date and cycle.
Plots and CSVs are saved to the specified output directory. The u & v component must be in the same file.
"""
    )

    parser.add_argument("--file", type=str, default=None,
                        help="Path or URL to a NetCDF file. If not provided, GFS 0.25° data will be fetched using --date and --cycle.")
    parser.add_argument("--date", type=str, default=datetime.datetime.now().strftime("%Y-%m-%d"),
                        help="Date for GFS data in YYYY-MM-DD format. Ignored if --file is provided.")
    parser.add_argument("--cycle", type=str, choices=["00z","06z","12z","18z"], default="00z",
                        help="GFS forecast cycle to use (00z, 06z, 12z, or 18z). Ignored if --file is provided.")
    parser.add_argument("--outdir", type=str, default="/home/index/GFS",
                        help="Directory to save CSVs and PNGs. Will be created automatically if it does not exist.")
    parser.add_argument("--indices", type=str, default="SWMI1,SWMI2,NEMI,NEMO,MESI",
                        help="Comma-separated list of indices to plot. Example: SWMI1,NEMI,MESI")
    return parser.parse_args()

# ------------------- MAIN -------------------

def main():
    args = parse_args()
    outdir = args.outdir
    os.makedirs(outdir, exist_ok=True)
    selected_indices = [idx.strip().upper() for idx in args.indices.split(",")]

    if args.file:
        ds = load_dataset(file=args.file)
        ct = datetime.datetime.now().date()
        adate = subtract_days_from_date(ct, 1)
    else:
        ct = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
        adate = subtract_days_from_date(ct, 1)
        adate1 = datetime.datetime.strptime(adate, "%d-%m-%Y")
        yyyy, mm, dd = adate1.strftime("%Y"), adate1.strftime("%m"), adate1.strftime("%d")
        ds = load_dataset(yyyy=yyyy, mm=mm, dd=dd, cycle=args.cycle)

    u850, u925, v925 = preprocess_winds(ds)

    if "SWMI1" in selected_indices:
        mia.plot_swmi1(u850, adate, ct, outdir)
    if "SWMI2" in selected_indices:
        mia.plot_swmi2(u850, adate, ct, outdir)
    if "NEMI" in selected_indices:
        mia.plot_nemi(u850, u925, adate, ct, outdir)
    if "NEMO" in selected_indices:
        mia.plot_nemo(v925, adate, ct, outdir)
    if "MESI" in selected_indices:
        mia.plot_mesi(u925, v925, adate, ct, outdir)

if __name__ == "__main__":
    main()
