from utils.data_convert import format_account_summary
from core import ib

if __name__ == "__main__":
    # get_fundamental_data("NVDA")
    # trades = place_limit_order("AAPL", 100, 100)
    # print(trades.order.orderId)

    # print(get_order_status())
    # print(get_account_summary())

    account_values = ib.accountValues()
    formatted_account_values = format_account_summary(account_values)
    print(formatted_account_values)
