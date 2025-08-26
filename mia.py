# mia.py
# Written by Diong Jeong Yik
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

sns.set(style="whitegrid")

# Helper to get the data column name
def df_column_name(data_array):
    return list(data_array.to_dataframe().columns)[0]

def plot_swmi1(u850, adate, ct, outdir):
    os.makedirs(outdir, exist_ok=True)
    box1 = u850.sel(lon=slice(90, 130), lat=slice(5, 15)).mean(dim=["lon", "lat"])
    box2 = u850.sel(lon=slice(100.75, 103.25), lat=slice(1.75, 4.25)).mean(dim=["lon", "lat"])
    swmi1 = box2 - box1
    df = swmi1.to_dataframe().reset_index()
    df.to_csv(f"{outdir}/swmi1_{adate}.csv", index=False)

    sns.lineplot(data=df, x="time", y=df_column_name(swmi1), marker="p")
    plt.title(f"SWMI1 Forecast Updated: {ct}", fontsize=10)
    plt.xlabel("Date", fontsize=8)
    plt.ylabel("SWMI1 (m/s)", fontsize=8)
    plt.xticks(rotation=90)
    plt.axhline(y=0.0, color="red", linestyle="--", linewidth=2)
    plt.tight_layout()
    plt.savefig(f"{outdir}/swmi1.png", bbox_inches="tight", dpi=300)
    plt.close("all")

def plot_swmi2(u850, adate, ct, outdir):
    os.makedirs(outdir, exist_ok=True)
    swmi2 = u850.sel(lon=slice(100, 115), lat=slice(5, 10)).mean(dim=["lon", "lat"])
    df = swmi2.to_dataframe().reset_index()
    df.to_csv(f"{outdir}/swmi2_{adate}.csv", index=False)

    sns.lineplot(data=df, x="time", y=df_column_name(swmi2), marker="p")
    plt.title(f"SWMI2 Forecast Updated: {ct}", fontsize=10)
    plt.xlabel("Date", fontsize=8)
    plt.ylabel("SWMI2 (m/s)", fontsize=8)
    plt.xticks(rotation=90)
    plt.axhline(y=0.0, color="red", linestyle="--", linewidth=2)
    plt.tight_layout()
    plt.savefig(f"{outdir}/swmi2.png", bbox_inches="tight", dpi=300)
    plt.close("all")

def plot_nemi(u850, u925, adate, ct, outdir):
    os.makedirs(outdir, exist_ok=True)
    n850 = u850.sel(lon=slice(102.5, 105), lat=slice(3.75, 6.25)).mean(dim=["lon", "lat"])
    n925 = u925.sel(lon=slice(102.5, 105), lat=slice(3.75, 6.25)).mean(dim=["lon", "lat"])
    df850 = n850.to_dataframe().reset_index().rename(columns={df_column_name(n850): "u850"})
    df925 = n925.to_dataframe().reset_index().rename(columns={df_column_name(n925): "u925"})
    df = pd.merge(df850, df925, on="time")
    df["average"] = df[["u850", "u925"]].mean(axis=1)
    df.to_csv(f"{outdir}/nemi_{adate}.csv", index=False)

    sns.lineplot(data=df, x="time", y="average", marker="p")
    plt.title(f"NEMI Forecast Updated: {ct}", fontsize=10)
    plt.xlabel("Date", fontsize=8)
    plt.ylabel("NEMI (m/s)", fontsize=8)
    plt.xticks(rotation=90)
    plt.axhline(y=-2.5, color="red", linestyle="--", linewidth=2)
    plt.tight_layout()
    plt.savefig(f"{outdir}/nemi.png", bbox_inches="tight", dpi=300)
    plt.close("all")

def plot_nemo(v925, adate, ct, outdir):
    os.makedirs(outdir, exist_ok=True)
    nemo = v925.sel(lon=slice(107, 115), lat=slice(5, 15)).mean(dim=["lon", "lat"])
    df = nemo.to_dataframe().reset_index()
    df.to_csv(f"{outdir}/nemo_{adate}.csv", index=False)

    sns.lineplot(data=df, x="time", y=df_column_name(nemo), marker="p")
    plt.title(f"NEMO Forecast Updated: {ct}", fontsize=10)
    plt.xlabel("Date", fontsize=8)
    plt.ylabel("NEMO (m/s)", fontsize=8)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(f"{outdir}/nemo.png", bbox_inches="tight", dpi=300)
    plt.close("all")

def plot_mesi(u925, v925, adate, ct, outdir):
    os.makedirs(outdir, exist_ok=True)
    esi = u925.sel(lon=120, lat=slice(7.5, 15)).mean(dim="lat")
    df_esi = esi.to_dataframe().reset_index()

    msi = v925.sel(lon=slice(110, 117.5), lat=15).mean(dim="lon")
    df_msi = msi.to_dataframe().reset_index()

    sns.lineplot(data=df_esi, x="time", y=df_column_name(esi), marker="p", label="ESI")
    sns.lineplot(data=df_msi, x="time", y=df_column_name(msi), marker="s", label="MSI")
    plt.title(f"MESI Forecast Analysis Time: {adate}", fontsize=10)
    plt.xlabel("Date", fontsize=8)
    plt.ylabel("u/v-wind (m/s)", fontsize=8)
    plt.xticks(rotation=90)
    plt.axhline(y=-8, color="red", linestyle="--", linewidth=2)
    plt.tight_layout()
    plt.savefig(f"{outdir}/mesi.png", bbox_inches="tight", dpi=300)
    plt.close("all")
