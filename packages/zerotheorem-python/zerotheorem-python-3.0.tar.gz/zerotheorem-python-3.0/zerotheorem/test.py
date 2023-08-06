import zerotheorem as zt
auth_token = "cd65a52ab8e2022697e0b93a199d7c60efcc036d75ce0591a86d2172998a44b3"
zt.authenticate(auth_token)
forecast = zt.get_stats("ZT1_SM8H_1")
print(forecast)