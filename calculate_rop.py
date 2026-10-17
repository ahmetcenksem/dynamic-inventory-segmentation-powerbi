"""Proje: Dinamik Stok Segmentasyonu ve Emniyet Stoku Modeli
Yazar: Ahmet Cenk Semerci
Metodoloji: Pareto Analizi (ABC), Varyasyon Katsayisi (XYZ) ve Dinamik ROP Modeli
"""

import numpy as np
import pandas as pd


def run_inventory_analysis(input_file, output_file):
    df = pd.read_csv(input_file)
    aylar = [f"Ay_{i}" for i in range(1, 13)]

    # 1. Talep & Ciro Metrikleri
    df["Toplam_Talep"] = df[aylar].sum(axis=1)
    df["Ortalama_Aylik_Talep"] = df[aylar].mean(axis=1)
    df["Std_Talep"] = df[aylar].std(axis=1)
    df["Toplam_Ciro"] = df["Toplam_Talep"] * df["Birim_Maliyet_TL"]
    df["Gunluk_Ortalama_Talep"] = df["Toplam_Talep"] / 365

    # 2. XYZ Segmentasyonu (Varyasyon Katsayısı)
    df["CV"] = (df["Std_Talep"] / df["Ortalama_Aylik_Talep"]).round(2)
    df["XYZ_Sinifi"] = np.where(
        df["CV"] <= 0.20, "X", np.where(df["CV"] <= 0.50, "Y", "Z")
    )

    # 3. ABC Segmentasyonu (Pareto Analizi)
    df = df.sort_values(by="Toplam_Ciro", ascending=False).reset_index(drop=True)
    df["Kumulatif_Ciro"] = df["Toplam_Ciro"].cumsum()
    df["Kumulatif_Yuzde"] = df["Kumulatif_Ciro"] / df["Toplam_Ciro"].sum()
    df["ABC_Sinifi"] = np.where(
        df["Kumulatif_Yuzde"] <= 0.70,
        "A",
        np.where(df["Kumulatif_Yuzde"] <= 0.90, "B", "C"),
    )
    df["Segment"] = df["ABC_Sinifi"] + df["XYZ_Sinifi"]

    # 4. Emniyet Stoku ve ROP (Z = 1.65 / %95 Servis Seviyesi)
    Z = 1.65
    df["Gunluk_Std"] = df["Std_Talep"] / np.sqrt(30)
    df["Emniyet_Stogu"] = np.ceil(
        Z * df["Gunluk_Std"] * np.sqrt(df["Tedarik_Suresi_Gun"])
    ).astype(int)
    df["ROP"] = np.ceil(
        (df["Gunluk_Ortalama_Talep"] * df["Tedarik_Suresi_Gun"])
        + df["Emniyet_Stogu"]
    ).astype(int)

    # 5. Karar Destek Çıktıları
    df["Siparis_Durumu"] = np.where(
        df["Mevcut_Stok"] <= df["ROP"], "Siparis Ver", "Stok Yeterli"
    )
    df["Onerilen_Siparis_Miktari"] = np.where(
        df["Mevcut_Stok"] <= df["ROP"], (df["ROP"] * 2) - df["Mevcut_Stok"], 0
    ).astype(int)

    cols_to_export = [
        "SKU",
        "Urun_Adi",
        "Kategori",
        "Birim_Maliyet_TL",
        "Tedarik_Suresi_Gun",
        "Mevcut_Stok",
        "Toplam_Talep",
        "Toplam_Ciro",
        "ABC_Sinifi",
        "CV",
        "XYZ_Sinifi",
        "Segment",
        "Emniyet_Stogu",
        "ROP",
        "Siparis_Durumu",
        "Onerilen_Siparis_Miktari",
    ]
    df[cols_to_export].to_csv(output_file, index=False)
    print(f"Optimizasyon tamamlandı. Çıktı: {output_file}")


if __name__ == "__main__":
    run_inventory_analysis("stok_verisi.csv", "stok_analizi_sonuc.csv")
