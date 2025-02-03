# go.Table(
#         header=dict(
#             values=["Date", "Number<br>Transactions", "Output<br>Volume (BTC)",
#                     "Market<br>Price", "Hash<br>Rate", "Cost per<br>trans-USD",
#                     "Mining<br>Revenue-USD", "Trasaction<br>fees-BTC"],
#             font=dict(size=10),
#             align="left"
#         ),
#         cells=dict(
#             values=[df[k].tolist() for k in df.columns[1:]],
#             align = "left")
#     ),
#     row=1, col=1