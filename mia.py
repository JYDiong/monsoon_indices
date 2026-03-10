# -*- coding: utf-8 -*-
# mia.py 
# Written by Diong Jeong Yik -updated 10 March 2026

import os
import xarray as xr
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style="whitegrid")


# --------------------------
# Helper function: select region and average
# --------------------------
def select_region(da, lon_range=None, lat_range=None, mean_dims=["lon","lat"]):
    """
    Select a region and average over mean_dims, handling:
    - lon/lat vs longitude/latitude names
    - ascending or descending coordinates
    """
    # Detect coordinate names
    lon_name = "lon" if "lon" in da.coords else "longitude" if "longitude" in da.coords else None
    lat_name = "lat" if "lat" in da.coords else "latitude" if "latitude" in da.coords else None

    sel_dict = {}
    if lon_range and lon_name:
        start, end = lon_range
        if da[lon_name][0] > da[lon_name][-1]:  # descending
            start, end = end, start
        sel_dict[lon_name] = slice(start, end)

    if lat_range and lat_name:
        start, end = lat_range
        if da[lat_name][0] > da[lat_name][-1]:  # descending
            start, end = end, start
        sel_dict[lat_name] = slice(start, end)

    if sel_dict:
        da = da.sel(sel_dict)

    # Average over available dims
    if mean_dims:
        mean_dims_existing = [d for d in mean_dims if d in da.dims]
        if mean_dims_existing:
            da = da.mean(dim=mean_dims_existing)

    return da


# --------------------------
# Plot engine
# --------------------------
def plot_region(layers, adate, ct, outdir, config):
    """
    layers: list of xarray DataArrays
    config: dictionary with optional keys:
        filename, ylabel, diff, dual, layer_labels, marker, hline
    """
    os.makedirs(outdir, exist_ok=True)

    filename = config.get("filename", "plot")
    ylabel = config.get("ylabel", filename)
    diff = config.get("diff", False)
    dual = config.get("dual", False)
    layer_labels = config.get("layer_labels", None)
    marker = config.get("marker", "o")
    hline = config.get("hline", None)

    # Compute difference if requested
    if diff:
        layers = [layers[1] - layers[0]]
        if not layer_labels:
            layer_labels = [filename]

    # Dual plot (2 layers)
    if dual and len(layers) == 2:
        da1, da2 = layers
        df1 = da1.to_dataframe().reset_index()
        df2 = da2.to_dataframe().reset_index()
        sns.lineplot(data=df1, x="time", y=list(df1.columns)[1],
                     marker=marker[0], label=layer_labels[0])
        sns.lineplot(data=df2, x="time", y=list(df2.columns)[1],
                     marker=marker[1], label=layer_labels[1])
        df1.to_csv(os.path.join(outdir, f"{filename}_{adate}.csv"), index=False)
        df2.to_csv(os.path.join(outdir, f"{filename}_{adate}_2.csv"), index=False)
    else:
        # Average multiple layers if >1
        if len(layers) > 1:
            dfs = []
            for i, da in enumerate(layers):
                df = da.to_dataframe().reset_index().rename(columns={list(da.to_dataframe().columns)[0]: f"layer{i}"})
                dfs.append(df)
            df_merged = dfs[0]
            for df in dfs[1:]:
                df_merged = pd.merge(df_merged, df, on="time")
            df_merged["average"] = df_merged[[f"layer{i}" for i in range(len(layers))]].mean(axis=1)
            df_merged.to_csv(os.path.join(outdir, f"{filename}_{adate}.csv"), index=False)
            sns.lineplot(data=df_merged, x="time", y="average", marker=marker if isinstance(marker,str) else marker[0])
        else:
            da = layers[0]
            df = da.to_dataframe().reset_index()
            df.to_csv(os.path.join(outdir, f"{filename}_{adate}.csv"), index=False)
            sns.lineplot(data=df, x="time", y=list(df.columns)[1], marker=marker if isinstance(marker,str) else marker[0])

    # Titles, labels, horizontal line
    plt.title(f"{ylabel} Forecast Updated: {ct}", fontsize=10)
    plt.xlabel("Date", fontsize=8)
    plt.ylabel(ylabel, fontsize=8)
    plt.xticks(rotation=90)
    if hline is not None:
        plt.axhline(y=hline, color="red", linestyle="--", linewidth=2)
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, f"{filename}.png"), bbox_inches="tight", dpi=300)
    plt.close("all")


# --------------------------
# MIA Index Functions
# --------------------------
def SWMI1(u850, adate, ct, outdir, config=None):
    default_config = {
        "filename": "swmi1",
        "ylabel": "SWMI1 (m/s)",
        "diff": True,
        "marker": "p",
        "hline": 0
    }
    cfg = {**default_config, **(config or {})}

    box1 = select_region(u850, lon_range=(90,130), lat_range=(5,15))
    box2 = select_region(u850, lon_range=(100.75,103.25), lat_range=(1.75,4.25))
    plot_region([box1, box2], adate, ct, outdir, cfg)


def SWMI2(u850, adate, ct, outdir, config=None):
    default_config = {
        "filename": "swmi2",
        "ylabel": "SWMI2 (m/s)",
        "marker": "p",
        "hline": 0
    }
    cfg = {**default_config, **(config or {})}

    box = select_region(u850, lon_range=(100,115), lat_range=(5,10))
    plot_region([box], adate, ct, outdir, cfg)


def NEMI(u850, u925, adate, ct, outdir, config=None):
    default_config = {
        "filename": "nemi",
        "ylabel": "NEMI (m/s)",
        "marker": "p",
        "hline": -2.5
    }
    cfg = {**default_config, **(config or {})}

    box1 = select_region(u850, lon_range=(102.5,105), lat_range=(3.75,6.25))
    box2 = select_region(u925, lon_range=(102.5,105), lat_range=(3.75,6.25))
    plot_region([box1, box2], adate, ct, outdir, cfg)


def NEMO(v925, adate, ct, outdir, config=None):
    default_config = {
        "filename": "nemo",
        "ylabel": "NEMO (m/s)",
        "marker": "p"
    }
    cfg = {**default_config, **(config or {})}

    box = select_region(v925, lon_range=(107,115), lat_range=(5,15))
    plot_region([box], adate, ct, outdir, cfg)


def MESI(u925, v925, adate, ct, outdir, config=None):
    default_config = {
        "filename": "mesi",
        "ylabel": "u/v-wind (m/s)",
        "dual": True,
        "layer_labels":["ESI","MSI"],
        "marker":["p","s"],
        "hline": -8
    }
    cfg = {**default_config, **(config or {})}

    # ESI: u925 at lon=120, lat 7.5-15
    esi = u925.sel(lon=120, lat=slice(7.5,15)).mean(dim="lat")
    # MSI: v925 at lat=15, lon 110-117.5
    msi = v925.sel(lon=slice(110,117.5), lat=15).mean(dim="lon")
    plot_region([esi, msi], adate, ct, outdir, cfg)
