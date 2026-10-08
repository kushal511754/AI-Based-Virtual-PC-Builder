"""Helper utilities."""

def format_price(price):
    """Format price as currency in INR."""
    # Convert database price to INR (1 USD = 83 INR)
    price_inr = int(price * 83)
    return f"₹{price_inr:,}"

def calculate_power_draw(cpu_tdp, gpu_power_draw):
    """Calculate total system power draw."""
    return cpu_tdp + gpu_power_draw

def get_performance_tier(cores, tdp):
    """Get CPU performance tier."""
    if cores >= 16:
        return "High-End"
    elif cores >= 8:
        return "Mid-Range"
    elif cores >= 4:
        return "Entry-Level"
    else:
        return "Budget"

def get_gpu_tier(vram_gb):
    """Get GPU tier based on VRAM."""
    if vram_gb >= 24:
        return "Flagship"
    elif vram_gb >= 12:
        return "High-End"
    elif vram_gb >= 8:
        return "Mid-Range"
    elif vram_gb >= 4:
        return "Entry-Level"
    else:
        return "Budget"
