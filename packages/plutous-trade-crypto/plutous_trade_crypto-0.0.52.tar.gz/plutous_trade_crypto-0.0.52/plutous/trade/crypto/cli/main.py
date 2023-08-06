import asyncio
from datetime import datetime, timedelta

from typer import Context, Typer

from plutous.cli.utils import parse_context_args
from plutous.enums import Exchange
from plutous.trade.crypto import alerts
from plutous.trade.crypto.collectors import COLLECTORS
from plutous.trade.crypto.enums import CollectorType

from . import database

app = Typer(name="crypto")
apps = [database.app]

for a in apps:
    app.add_typer(a)


@app.command()
def collect(
    exchange: Exchange,
    collector_type: CollectorType,
    rate_limit: bool = False,
):
    """Collect data from exchange."""
    collector = COLLECTORS[collector_type](exchange, rate_limit=rate_limit)
    asyncio.run(collector.collect())


@app.command()
def backfill(
    exchange: Exchange,
    collector_type: CollectorType,
):
    """Backfill last 1-hour data from exchange."""
    collector = COLLECTORS[collector_type](exchange)

    since = datetime.now() - timedelta(hours=1)
    asyncio.run(collector.backfill(since))


@app.command(
    context_settings={
        "allow_extra_args": True,
        "ignore_unknown_options": True,
    }
)
def alert(
    alert_type: str,
    ctx: Context,
):
    """Alert on data from exchange."""
    alert_cls = getattr(alerts, f"{alert_type}Alert")
    alert_config_cls = getattr(alerts, f"{alert_type}AlertConfig")

    config = alert_config_cls(**parse_context_args(ctx))
    alert = alert_cls(config)
    alert.run()
