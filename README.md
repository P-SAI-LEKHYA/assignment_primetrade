# Production-Grade Binance Futures Testnet Trading Engine Terminal

An enterprise-grade, lightweight implementation of a simplified trading execution layer operating across the **Binance Futures Testnet (USDT-M)** ecosystem. This application is structured to decouple interface workflows from deep network abstractions, providing robust pre-flight validation, exception tolerance, and structured dual-destination telemetry logging.

---

# 🔥 Key Architectural Highlights

- **Decoupled Multi-Layer Architecture**
  - Network & Authentication (`bot/client.py`)
  - Business Logic (`bot/orders.py`)
  - Input Validation (`bot/validators.py`)
  - Logging (`bot/logging_config.py`)
  - CLI Interface (`cli.py`)

- **Enhanced Interactive Terminal (Bonus)**
  - Built using **Questionary** and **Rich**
  - Arrow-key navigation
  - Loading spinners
  - Color-coded execution summaries

- **Pre-Flight Validation**
  - Validates user inputs before API requests
  - Prevents unnecessary network calls
  - Reduces chances of API rejection

- **Dual-Destination Logging**
  - Console displays clean execution summaries
  - Detailed logs stored in `logs/trading_bot.log`

---

# 💡 System Assumptions

The following assumptions were made during development:

1. The application targets only the **Binance USDT-M Futures Testnet** endpoint:
   ```
   https://testnet.binancefuture.com
   ```

2. Users possess valid Binance Testnet API credentials.

3. Authentication uses Binance's standard **HMAC SHA256 signature** mechanism.

4. LIMIT orders returning

   - Status = `NEW`
   - Avg Price = `0.0`

   are considered successful because the order has been accepted but not yet matched.

5. Users maintain sufficient virtual margin in their Testnet account before placing orders.

---

# 📁 Project Structure

```text
trading_bot/
│
├── bot/
│   ├── __init__.py
│   ├── client.py
│   ├── orders.py
│   ├── validators.py
│   └── logging_config.py
│
├── logs/
│   └── trading_bot.log
│
├── cli.py
├── requirements.txt
└── README.md
```

---

# 🛠 Installation

## 1. Clone Repository

```bash
git clone <your-public-github-repo-url>
cd trading_bot
```

---

## 2. Create Virtual Environment

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a file named `.env` in the project root.

```env
BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_api_secret
```

> **Note**
>
> - Do not use quotes.
> - Do not leave spaces around `=`.

---

# 🚀 Running the Application

## Interactive Mode

Launch the terminal interface:

```bash
python cli.py
```

The application will guide you through:

- Symbol selection
- Order Side
- Order Type
- Quantity
- Price (for LIMIT orders)

using an interactive menu.

---

## Command Line Mode

### MARKET Order

```bash
python cli.py \
--symbol BTCUSDT \
--side BUY \
--type MARKET \
--qty 0.002
```

### LIMIT Order

```bash
python cli.py \
--symbol ETHUSDT \
--side SELL \
--type LIMIT \
--qty 0.05 \
--price 3500
```

---

# 📊 Logging

The application writes logs to two locations.

## Console

Displays:

- Order status
- Success messages
- Errors
- Execution summary

---

## Log File

```
logs/trading_bot.log
```

Contains:

- Timestamp
- API endpoint
- Request payload
- HTTP response
- Exceptions
- Authentication events

---

# ✅ Features

- Binance Futures Testnet Integration
- MARKET Orders
- LIMIT Orders
- Interactive CLI
- Command Line Support
- Input Validation
- Structured Logging
- HMAC SHA256 Authentication
- Rich Terminal UI
- Questionary-based Menu Navigation

---
# 📄 Sample Execution Output

## MARKET Order

```text
$ python cli.py

╭──────────────────────────────────────────╮
│ Binance Futures Testnet Trading Terminal │
╰──────────────────────────────────────────╯

? Enter Target Symbol (e.g., BTCUSDT): BTCUSDT
? Select Transaction Side: BUY
? Select Execution Type: MARKET
? Specify Order Quantity: 0.002

✔ Order Executed Successfully!

          Execution Statement Summary
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Parameter          ┃ Value                  ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Order ID           │ 21825110519            │
│ Client Order ID    │ qjNQOcREiLuV5g5M6N0qag │
│ Symbol             │ BTCUSDT                │
│ Status             │ NEW                    │
│ Side               │ BUY                    │
│ Type               │ MARKET                 │
│ Executed Qty       │ 0.0000                 │
│ Avg Price Spoke    │ 0.0                    │
└────────────────────┴────────────────────────┘
```

---

## LIMIT Order

```text
$ python cli.py

╭──────────────────────────────────────────╮
│ Binance Futures Testnet Trading Terminal │
╰──────────────────────────────────────────╯

? Enter Target Symbol (e.g., BTCUSDT): BTCUSDT
? Select Transaction Side: BUY
? Select Execution Type: LIMIT
? Specify Order Quantity: 0.002
? Enter Target Execution Price Limit: 65000

✔ Order Executed Successfully!

          Execution Statement Summary
┏━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Parameter          ┃ Value                  ┃
┡━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Order ID           │ 21825548756            │
│ Client Order ID    │ sLABrxBpM7tU0hfppfOsKc │
│ Symbol             │ BTCUSDT                │
│ Status             │ NEW                    │
│ Side               │ BUY                    │
│ Type               │ LIMIT                  │
│ Executed Qty       │ 0.0000                 │
│ Avg Price Spoke    │ 0.0                    │
└────────────────────┴────────────────────────┘
```

---

## 📌 Note

The Binance Futures Testnet may initially return:

- **Status:** `NEW`
- **Executed Qty:** `0.0000`
- **Average Price:** `0.0`

This indicates that the exchange has **accepted the order successfully**, but no execution has occurred yet. On the Testnet, MARKET orders may also briefly appear with `NEW` status before being processed, depending on the simulated matching engine behavior.

# 📦 Dependencies

- requests
- rich
- questionary
- python-dotenv

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---




# 📝 Notes

- This project is intended **only for Binance Futures Testnet**.
- No real funds are involved.
- Ensure sufficient Testnet balance before placing orders.
- LIMIT orders remain in the order book until matched or cancelled.

---

# 📜 License

This project is developed for educational and assessment purposes.
