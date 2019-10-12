import airsim

client = airsim.MultirotorClient()

client.confirmConnection()

client.enableApiControl(True)
client.armDisarm(True)



client.takeoffAsync().join()

client.simEnableWeather(True)
#client.moveToPositionAsync(0, 0,-2, 10,yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=90),drivetrain=airsim.DrivetrainType.MaxDegreeOfFreedom).join()
client.simSetWeatherParameter(airsim.WeatherParameter.Rain, 0.25);
client.simSetWeatherParameter(airsim.WeatherParameter.Dust, 0.50);

client.moveToPositionAsync(100, 0,-2, 5,yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=90),drivetrain=airsim.DrivetrainType.MaxDegreeOfFreedom).join()

client.simEnableWeather(False)

client.moveToPositionAsync(0, 0,-2, 5,yaw_mode=airsim.YawMode(is_rate=False, yaw_or_rate=90),drivetrain=airsim.DrivetrainType.MaxDegreeOfFreedom).join()

client.reset()
