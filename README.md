# 智能温室大棚

### 硬件部分
1. 树莓派
2. 光敏电阻
3. DHT11
4. 水泵
5. 继电器

### 模块程序
1. 继电器: `HActuator.HRELAY(pin: int, trigger: bool = False)`
2. DHT模块: `HSensors.DHT(pin: int, dht_type = 'DHT11')`
3. 步进电机: `HActuator.SteeppingMOTOR(pins: list[int])`

### 光照-遮光帘控制模块
1. 自动模式下: 亮度 **低于** 阈值时，设置遮光帘为 **打开** 的状态
2. 自动模式下: 亮度 **高于** 阈值时，设置遮光帘为 **关闭** 的状态
