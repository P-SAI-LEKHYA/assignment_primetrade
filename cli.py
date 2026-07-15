import os
import sys
import argparse
import questionary
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from bot.logging_config import setup_logging
from bot.client import BinanceFuturesClient
from bot.orders import OrderManager
from dotenv import load_dotenv  # <-- Fixed: Removed the nonexistent load_wrapper

load_dotenv()  # Looks for your .env file and securely injects your keys!

console = Console()

def get_credentials():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    if not api_key or not api_secret:
        console.print("[bold red]Error: Environment variables BINANCE_API_KEY and BINANCE_API_SECRET must be configured.[/bold red]")
        sys.exit(1)
    return api_key, api_secret

def render_success_ui(response: dict):
    console.print("\n[bold green]✔ Order Executed Successfully![/bold green]\n")
    
    table = Table(title="Execution Statement Summary", show_header=True, header_style="bold magenta")
    table.add_column("Parameter", style="dim", width=18)
    table.add_column("Value", style="cyan")
    
    table.add_row("Order ID", str(response.get("orderId")))
    table.add_row("Client Order ID", str(response.get("clientOrderId")))
    table.add_row("Symbol", str(response.get("symbol")))
    table.add_row("Status", f"[bold green]{response.get('status')}[/bold green]")
    table.add_row("Side", str(response.get("side")))
    table.add_row("Type", str(response.get("type")))
    table.add_row("Executed Qty", str(response.get("executedQty")))
    table.add_row("Avg Price Spoke", str(response.get("avgPrice", "0.0")))
    
    console.print(table)
    console.print("\n")

def run_interactive_menu(order_manager: OrderManager):
    console.print(Panel.fit("[bold cyan]Binance Futures Testnet Trading Terminal[/bold cyan]", border_style="cyan"))
    
    symbol = questionary.text("Enter Target Symbol (e.g., BTCUSDT):", default="BTCUSDT").ask()
    if not symbol: return

    side = questionary.select("Select Transaction Side:", choices=["BUY", "SELL"]).ask()
    order_type = questionary.select("Select Execution Type:", choices=["MARKET", "LIMIT"]).ask()
    
    qty_str = questionary.text("Specify Order Quantity:").ask()
    try:
        quantity = float(qty_str)
    except ValueError:
        console.print("[bold red]Invalid quantity input number.[/bold red]")
        return

    price = None
    if order_type == "LIMIT":
        price_str = questionary.text("Enter Target Execution Price Limit:").ask()
        try:
            price = float(price_str)
        except ValueError:
            console.print("[bold red]Invalid limit price structure input.[/bold red]")
            return

    try:
        with console.status("[bold yellow]Transmitting order payload to Binance Core Testnet engine...[/bold yellow]"):
            res = order_manager.create_order(symbol, side, order_type, quantity, price)
        render_success_ui(res)
    except Exception as e:
        console.print(Panel(f"[bold red]Execution Fault Action Blocked:[/bold red]\n{str(e)}", title="API Order Failure Error", border_style="red"))

def main():
    setup_logging()
    api_key, api_secret = get_credentials()
    
    client = BinanceFuturesClient(api_key, api_secret)
    order_manager = OrderManager(client)
    
    # Optional setup layer checking fallback for script/automation operations.
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description="Automated Execution Backend Module Engine Tools Verification CLI Mode")
        parser.add_argument("--symbol", required=True, help="Trading pair string (e.g., ETHUSDT)")
        parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order execution target direction side")
        parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT"], help="Order execution style strategy type")
        parser.add_argument("--qty", required=True, type=float, help="Volume execution targets size value")
        parser.add_argument("--price", type=float, default=None, help="Execution target trigger value layer required for LIMIT executions")
        
        args = parser.parse_args()
        try:
            res = order_manager.create_order(args.symbol, args.side, args.type, args.qty, args.price)
            render_success_ui(res)
        except Exception as e:
            console.print(f"[bold red]Automated Order Fault Failure Event Logs Profiled: {e}[/bold red]")
    else:
        run_interactive_menu(order_manager)

if __name__ == "__main__":
    main()