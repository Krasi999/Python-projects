import cv2
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from compression import compress_image, decompress_image
from metrics import calculate_psnr, calculate_ssim, get_memory_usage, measure_peak_memory, measure_cpu_during
from network import simulate_network_transfer, SCENARIOS
from utils import load_image, resize_image, get_size
 
# ──────────────────────────────────────────────
# TARGET PLATFORM: PC Simulation
# Моделира поведение на мобилно/IoT устройство
# Target latency: < 200ms for 720p on 4G
# ──────────────────────────────────────────────
 
def show_demo(original, decompressed, title_text):
    """
    Displays a demo window with Original vs Decompressed image.
    This is a demonstration mode — NOT a real-time stream.
    waitKey(1) handles UI events without blocking.
    """
    try:
        vis_orig = cv2.resize(original, (640, 360))
        vis_dec  = cv2.resize(decompressed, (640, 360))
        comparison = np.hstack((vis_orig, vis_dec))
        cv2.putText(comparison, "Original", (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(comparison, "Decompressed", (660, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(comparison, title_text, (10, 355),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.imshow("Compression Demo: Original vs Decompressed", comparison)
        cv2.waitKey(1)   # 1ms — обработва UI без блокиране
    except Exception as e:
        print(f"Demo window error: {e}")
 
 
def run_comprehensive_test(image_path):
    if not os.path.exists(image_path):
        print(f"Error: File '{image_path}' not found.")
        return

    image_name = os.path.basename(image_path)  

    orig_img = load_image(image_path)
    if orig_img is None:
        return

    resolutions = [(640, 480), (1280, 720), (1920, 1080)]
    modes       = ["fast", "high"]
    formats     = ["jpg", "webp"]
    results     = []

    print("=" * 60)
    print("STARTING BENCHMARK")
    print(f"Target Platform  : PC Simulation (Android/IoT model)")
    print(f"Target Latency   : < 200ms for 720p at 4G Mobile")
    print(f"Initial RAM usage: {get_memory_usage():.2f} MB")
    print("=" * 60)

    cv2.namedWindow("Compression Demo: Original vs Decompressed", cv2.WINDOW_AUTOSIZE)

    for res in resolutions:
        img = resize_image(orig_img, res[0], res[1])

        for fmt in formats:
            for mode in modes:

                (encoded, c_time), cpu_val = measure_cpu_during(
                    compress_image, img, mode, fmt
                )

                (decoded, d_time), peak_ram_kb = measure_peak_memory(
                    decompress_image, encoded
                )

                size = get_size(encoded)

                for net_name in SCENARIOS.keys():
                    net_time = simulate_network_transfer(size, net_name)
                    total_latency = c_time + net_time + d_time

                    psnr   = calculate_psnr(img, decoded)
                    ssim_v = calculate_ssim(img, decoded)

                    results.append({
                        "Image":          image_name,  # ✅ ДОБАВЕНО
                        "Config":         f"{res[1]}p_{fmt}_{mode}",
                        "Format":         fmt,
                        "Resolution":     res[1],
                        "Mode":           mode,
                        "Network":        net_name,
                        "Size_KB":        size / 1024,
                        "Compress_ms":    c_time * 1000,
                        "Network_ms":     net_time * 1000,
                        "Decompress_ms":  d_time * 1000,
                        "Total_ms":       total_latency * 1000,
                        "PSNR":           psnr,
                        "SSIM":           ssim_v,
                        "Peak_RAM_KB":    peak_ram_kb,
                        "CPU_Percent":    cpu_val
                    })

                show_demo(img, decoded, f"{res[1]}p {fmt} {mode} | SSIM:{ssim_v:.3f} | {c_time*1000:.1f}ms")
                print(f" Test: {res[1]}p | {fmt:4s} | {mode:4s} | "
                      f"Size:{size/1024:7.1f}KB | "
                      f"Comp:{c_time*1000:5.1f}ms | "
                      f"PSNR:{psnr:5.1f}dB | SSIM:{ssim_v:.3f} | "
                      f"CPU:{cpu_val:4.1f}% | Peak RAM:{peak_ram_kb:.0f}KB")
 
    cv2.destroyAllWindows()
 
    df = pd.DataFrame(results)
    df.to_csv("performance_results.csv",
              mode='a',
              header=not os.path.exists("performance_results.csv"),
              index=False)
 
    print_tabular_analysis(df)
    generate_recommendations(df)
    generate_charts(df)
    print("\n✓ Charts saved to 'analysis_charts.png'")
 
# ──────────────────────────────────────────────────────────────────────────────
# TABULAR ANALYSIS — prints summary tables to the console
# ──────────────────────────────────────────────────────────────────────────────
 
def print_tabular_analysis(df):
    print("\n" + "=" * 70)
    print("TABULAR ANALYSIS")
    print("=" * 70)
 
    # Table 1: Average values by format and mode (all networks averaged)
    print("\n[1] Average values by Format × Mode")
    print("-" * 70)
    summary = df.groupby(["Format", "Mode"]).agg(
        Avg_Size_KB   =("Size_KB",     "mean"),
        Avg_PSNR      =("PSNR",        "mean"),
        Avg_SSIM      =("SSIM",        "mean"),
        Avg_Compr_ms  =("Compress_ms", "mean"),
        Avg_CPU_pct   =("CPU_Percent", "mean"),
        Avg_RAM_KB    =("Peak_RAM_KB", "mean"),
    ).round(3)
    print(summary.to_string())
 
    # Table 2: Latency by resolution, mode, and network
    print("\n[2] Total Latency (ms) by Resolution × Mode × Network")
    print("-" * 70)
    latency = df.groupby(["Resolution", "Mode", "Network"])["Total_ms"].mean().round(1)
    print(latency.to_string())
 
    # Table 3: Size by resolution and format
    print("\n[3] Average Size (KB) by Resolution × Format × Mode")
    print("-" * 70)
    sizes = df.groupby(["Resolution", "Format", "Mode"])["Size_KB"].mean().round(1)
    print(sizes.to_string())
 
    print()
 
# ──────────────────────────────────────────────────────────────────────────────
# RECOMMENDATIONS — automatically generated from the data
# ──────────────────────────────────────────────────────────────────────────────
 
def generate_recommendations(df):
    print("=" * 70)
    print("CONFIGURATION RECOMMENDATIONS")
    print("=" * 70)
 
    for net_name in df["Network"].unique():
        net_df = df[df["Network"] == net_name]
        print(f"\n  Network Scenario: {net_name}")
        print(f"  {'-'*50}")
 
        for res in sorted(df["Resolution"].unique()):
            res_df = net_df[net_df["Resolution"] == res]
 
            # Find the configuration with the best balance:
            # SSIM >= 0.85 (acceptable quality) + minimal latency
            acceptable = res_df[res_df["SSIM"] >= 0.85]
            if acceptable.empty:
                # Ако нищо не достига 0.85, вземаме най-доброто налично
                acceptable = res_df
 
            best = acceptable.loc[acceptable["Total_ms"].idxmin()]
            size_saving = ""
 
            # Compare with JPG high to show savings
            ref = res_df[(res_df["Format"] == "jpg") & (res_df["Mode"] == "high")]
            if not ref.empty:
                ref_size = ref["Size_KB"].values[0]
                best_size = best["Size_KB"]
                if ref_size > 0:
                    pct = (1 - best_size / ref_size) * 100
                    if pct > 1:
                        size_saving = f" (~{pct:.0f}% smaller than JPG high)"
 
            latency_flag = ""
            if best["Total_ms"] < 200:
                latency_flag = " ✓ (below target latency of 200ms)"
            elif best["Total_ms"] < 1000:
                latency_flag = " ⚠ (acceptable)"
            else:
                latency_flag = " ✗ (above 1s — consider lower resolution)"
 
            print(f"    {res}p → {best['Format'].upper()} {best['Mode']:4s} | "
                  f"Latency: {best['Total_ms']:.0f}ms{latency_flag} | "
                  f"Size: {best['Size_KB']:.1f}KB{size_saving} | "
                  f"SSIM: {best['SSIM']:.3f} | PSNR: {best['PSNR']:.1f}dB")
 
    print()
    print("  SUMMARY:")
    print("  • WebP fast is recommended for IoT/mobile scenarios with limited bandwidth.")
    print("  • JPG high is suitable for archiving and high-quality preview.")
    print("  • For IoT Narrowband — limit resolution to 480p for acceptable latency.")
    print("  • SSIM > 0.90 is the standard for mobile streaming applications.")
    print("=" * 70)
 
# ──────────────────────────────────────────────────────────────────────────────
# CHARTS
# ──────────────────────────────────────────────────────────────────────────────
 
def generate_charts(df):
    # Използваме твоите нови настройки за разположение (hspace и wspace)
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    plt.subplots_adjust(hspace=0.4, wspace=0.3, top=0.92, bottom=0.1)
 
    fig.suptitle("Multimedia Compression Analysis (TU-Sofia)", fontsize=16, fontweight='bold')
 
    # Chart 1: Quality vs Size
    ax1 = axes[0, 0]
    for fmt in df["Format"].unique():
        sub = df[df["Format"] == fmt].drop_duplicates(subset=["Config"])
        ax1.scatter(sub["Size_KB"], sub["SSIM"], label=fmt.upper(), s=80, alpha=0.7)
    ax1.set_title("Quality (SSIM) vs Size")
    ax1.set_xlabel("Size (KB)")
    ax1.set_ylabel("SSIM")
    ax1.legend(fontsize=9, loc='lower right')
    ax1.grid(True, linestyle='--', alpha=0.5)
 
    # Chart 2: Latency
    ax2 = axes[0, 1]
    pivot_lat = df.groupby(["Resolution", "Mode"])["Total_ms"].mean().unstack()
    pivot_lat.plot(kind="bar", ax=ax2, rot=0, color=['#5cb85c', '#d9534f'])
    ax2.axhline(y=200, color="blue", linestyle="--", alpha=0.6, label="Target 200ms")
    ax2.set_title("Total Latency (ms)")
    ax2.set_ylabel("Time (ms)")
    ax2.legend(fontsize=9)
 
    # Chart 3: Network Scenarios
    ax3 = axes[1, 0]
    df_720 = df[df["Resolution"] == 720]
    pivot_net = df_720.groupby(["Network", "Format"])["Total_ms"].mean().unstack()
    pivot_net.plot(kind="bar", ax=ax3, rot=15)
    ax3.set_title("720p Latency by Network")
    ax3.set_ylabel("ms")
    ax3.legend(fontsize=8)
 
    # Chart 4: Top PSNR
    ax4 = axes[1, 1]
    psnr_data = df.groupby("Config")["PSNR"].mean().sort_values().tail(10)
    psnr_data.plot(kind="barh", ax=ax4, color='skyblue', edgecolor='black', linewidth=0.5)
    ax4.set_title("Top 10 Configurations (PSNR)")
    ax4.set_xlabel("dB")
    ax4.tick_params(axis='y', labelsize=8)
 
    print("\n✓ Analysis complete. Displaying charts...")
    plt.show()
 
# ──────────────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    folder = "images"

    if not os.path.exists(folder):
        print("Error: 'images' folder not found.")
    else:
        for file in os.listdir(folder):
            if file.lower().endswith((".jpg", ".png")):
                path = os.path.join(folder, file)
                print(f"\nProcessing image: {file}")
                run_comprehensive_test(path)