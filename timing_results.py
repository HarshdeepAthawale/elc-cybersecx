"""
ELC Secure Network Configuration - Timing Graph Generator
Generates bar charts for encryption and decryption times.
"""

from pathlib import Path

BASE_DIR = Path(__file__).parent
ENCRYPTION_GRAPH = BASE_DIR / "encryption_time.png"
DECRYPTION_GRAPH = BASE_DIR / "decryption_time.png"


def generate_graphs(timings: dict[str, dict[str, float]]) -> None:
    """Generate PNG bar charts for encryption and decryption times."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed. Run: pip install matplotlib")
        return

    algorithms = list(timings.keys())
    encrypt_times = [timings[a]["encrypt"] for a in algorithms]
    decrypt_times = [timings[a]["decrypt"] for a in algorithms]

    # Encryption time chart
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(algorithms, encrypt_times, color=["#2ecc71", "#3498db", "#9b59b6"])
    ax.set_ylabel("Time (ms)")
    ax.set_title("Encryption Time by Algorithm")
    ax.set_ylim(0, max(encrypt_times) * 1.2)
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{height:.2f}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha="center",
                    fontsize=10)
    plt.tight_layout()
    plt.savefig(ENCRYPTION_GRAPH, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved {ENCRYPTION_GRAPH}")

    # Decryption time chart
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(algorithms, decrypt_times, color=["#2ecc71", "#3498db", "#9b59b6"])
    ax.set_ylabel("Time (ms)")
    ax.set_title("Decryption Time by Algorithm")
    ax.set_ylim(0, max(decrypt_times) * 1.2)
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{height:.2f}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha="center",
                    fontsize=10)
    plt.tight_layout()
    plt.savefig(DECRYPTION_GRAPH, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved {DECRYPTION_GRAPH}")


if __name__ == "__main__":
    # Demo: generate from sample data if no timings passed
    sample_timings = {
        "Caesar": {"encrypt": 12.5, "decrypt": 11.8},
        "Playfair": {"encrypt": 45.2, "decrypt": 44.1},
        "Hill": {"encrypt": 89.3, "decrypt": 95.7},
    }
    generate_graphs(sample_timings)
    print("Done. Run main.py and choose option 3 for real timing data.")
