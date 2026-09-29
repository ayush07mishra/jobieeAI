from app.collectors.greenhouse import GreenhouseCollector


def create_collector(company):

    platform = company["platform"]

    if platform == "greenhouse":

        return GreenhouseCollector(
            company_name=company["name"],
            board_token=company["board_token"]
        )

    raise ValueError(
        f"Unsupported platform: {platform}"
    )