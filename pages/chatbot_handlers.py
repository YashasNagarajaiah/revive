def handle_total_weight(metrics):
    """Handle total weight collection queries"""
    date_range = f"{metrics['dates']['earliest'].strftime('%B %d, %Y')} to {metrics['dates']['latest'].strftime('%B %d, %Y')}"
    return (
        f"Total Weight Collection Analysis (by Zain):\n\n"
        f"• Total Weight Collected: {metrics['total_weight']:,.2f} Kg\n"
        f"• Time Period: {date_range}\n"
        f"• Current Month Weight: {metrics['monthly']['current']['weight']:,.2f} Kg\n"
        f"• Previous Month Weight: {metrics['monthly']['previous']['weight']:,.2f} Kg\n"
        f"• Month-over-Month Growth: {metrics['growth']['weight']:+.1f}%"
    )

def handle_composition(metrics):
    """Handle waste composition queries"""
    response = ["Waste Stream Composition Analysis (by Zain):"]
    for stream, data in metrics['composition'].items():
        response.append(
            f"\n{stream}:"
            f"\n• Total Weight: {data['total_weight']:,.2f} Kg"
            f"\n• Percentage: {data['percentage']:.1f}%"
            f"\n• Collections: {data['collections']:,}"
            f"\n• Average Weight per Collection: {data['average_weight']:.2f} Kg"
        )
    return "\n".join(response)

def handle_collections(metrics):
    """Handle collection queries"""
    days = (metrics['dates']['latest'] - metrics['dates']['earliest']).days + 1
    avg_per_day = metrics['total_collections'] / days
    return (
        f"Collection Statistics (by Zain):\n\n"
        f"• Total Collections: {metrics['total_collections']:,}\n"
        f"• Current Month Collections: {metrics['monthly']['current']['collections']:,}\n"
        f"• Previous Month Collections: {metrics['monthly']['previous']['collections']:,}\n"
        f"• Collection Growth: {metrics['growth']['collections']:+.1f}%\n"
        f"• Average Collections Per Day: {avg_per_day:.1f}"
    )

def handle_environmental(metrics):
    """Handle environmental impact queries"""
    response = [
        f"Environmental Impact Analysis (by Zain):\n",
        f"• Total CO2 Prevented: {metrics['environmental']['co2_prevented']:,.2f} Kg",
        f"• Carbon Reduction: {metrics['environmental']['carbon_reduced']:,.2f} Kg",
        f"• Trees Equivalent: {metrics['environmental']['trees_equivalent']:.1f}",
        "\nBreakdown by Waste Stream:"
    ]
    for stream, impact in metrics['environmental']['by_stream'].items():
        response.append(f"• {stream}: {impact['co2']:,.2f} Kg CO2")
    return "\n".join(response)

def handle_monthly(metrics):
    """Handle monthly performance queries"""
    return (
        f"Monthly Performance Analysis (by Zain):\n"
        f"\nCurrent Month ({metrics['monthly']['current']['month']}):"
        f"\n• Weight: {metrics['monthly']['current']['weight']:,.2f} Kg"
        f"\n• Collections: {metrics['monthly']['current']['collections']:,}"
        f"\n\nPrevious Month ({metrics['monthly']['previous']['month']}):"
        f"\n• Weight: {metrics['monthly']['previous']['weight']:,.2f} Kg"
        f"\n• Collections: {metrics['monthly']['previous']['collections']:,}"
        f"\n\nGrowth Rates:"
        f"\n• Weight Growth: {metrics['growth']['weight']:+.1f}%"
        f"\n• Collection Growth: {metrics['growth']['collections']:+.1f}%"
    )

def get_help_message():
    """Return help message"""
    return 