import time
import smbus

class DHT20:
    """
    temperature and humidity sensora
    """    
    def __init__(self, bus_id=1):
        self.i2c = smbus.SMBus(bus_id)

        self.address = 0x38
        self.trigger = [0xAC, 0x33, 0x00]

        dat = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        ret = self.i2c.read_byte_data(self.address, 0x71)

    def read(self):
        self.i2c.write_i2c_block_data(self.address, 0x00, self.trigger)

        #データ読み取り
        time.sleep(0.08)
        dat = self.i2c.read_i2c_block_data(self.address, 0x00, 7)


        #データ格納
        hum = dat[1] << 12 | dat[2] << 4 | ((dat[3] & 0xF0) >> 4)
        tmp = ((dat[3] & 0x0F) << 16) | dat[4] << 8 | dat[5]
      
        #湿度変換  
        hum = hum / 2**20 * 100
        #温度変換
        tmp = tmp / 2**20 * 200 - 50
        return tmp, hum