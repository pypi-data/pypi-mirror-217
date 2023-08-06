#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Email : 807447312@qq.com
@Time  : 2023/7/5 22:15
@File  : MonitorCANBus.py
'''

import can

# 定义CAN接口
can_interface = 'can0'

# 定义CAN总线
bus = can.interface.Bus(can_interface,app_name='CANalyzer', bustype='vector')

# 发送诊断服务请求：获取ECU名称和ID
service_id = 0x22
sub_function = 0x83
data = [0xF1, 0x90, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
msg = can.Message(arbitration_id=0x7DF, data=[service_id, sub_function] + data, is_extended_id=False)
bus.send(msg)

# 等待并处理ECU的响应
while True:
    response_msg = bus.recv()
    if response_msg.arbitration_id == 0x7E8 and response_msg.data[0] == 0x62 and response_msg.data[1] == sub_function:
        ecu_list = []
        index = 2
        while index < len(response_msg.data):
            ecu_id = (response_msg.data[index] << 16) | (response_msg.data[index+1] << 8) | response_msg.data[index+2]
            index += 3
            ecu_name_len = response_msg.data[index]
            index += 1
            ecu_name = ''.join([chr(byte) for byte in response_msg.data[index:index+ecu_name_len] if byte != 0])
            index += ecu_name_len
            ecu_list.append({'id': ecu_id, 'name': ecu_name})
        break

# 打印所有ECU的名称和ID
print('Found %d ECU(s):' % len(ecu_list))
for ecu in ecu_list:
    print('  - ID: 0x%06X, Name: %s' % (ecu['id'], ecu['name']))
