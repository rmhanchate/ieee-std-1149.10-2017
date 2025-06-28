# -*- coding: utf-8 -*-
import binascii as bn

def read_file(filename):
    # reads data from the file
    
    print('Loading Bitstream from file ', filename)
    f = open(filename)
    line = f.read()
    f.close()
    
    return line


def write_file(filename, s):
    # writes data to a file
    
    print('Writing Bitstream to file', filename)
    f = open(filename, 'w')
    f.write(s)
    f.close()

def logger(s):
    # appends data to a file
    
    f = open('output.log', 'a')
    f.write(s + '\n\n')
    f.close()

def print_dict(dictionary):
    # displays a dictionary in a neat hierarchial manner
    # used for printing the attributes
    
    for attribute in dictionary:
        print(attribute, ':')
        for subattribute in dictionary[attribute]:
            if type(dictionary[attribute][subattribute]) == dict:
                print('\t', subattribute, ':')
                for innersubattribute in dictionary[attribute][subattribute]:
                    if type(dictionary[attribute][subattribute][innersubattribute]) == dict:
                        print('\t\t', innersubattribute, ':')
                        for innerinnersubattribute in dictionary[attribute][subattribute][innersubattribute]:
                            print('\t\t\t', innerinnersubattribute, ':', dictionary[attribute][subattribute][innersubattribute][innerinnersubattribute])
                    else:
                        print('\t\t', innersubattribute, ':', dictionary[attribute][subattribute][innersubattribute])
            else:
                print('\t', subattribute, ':', dictionary[attribute][subattribute])


def hexstr(bit, number):
    # returns a hex string padded to specified number of bits
    
    for _ in range(bit - len(number[2:])):
        number = '0x0' + number[2:]
        
    return number

def binstr(bit, number):
    # returns a binary string padded to specified number of bits
    
    for _ in range(bit - len(number[2:])):
        number = '0b0' + number[2:]
        
    return number  


class ieeestd(object):
    # main ieee 1149.10 state object used in all states.
    # provides some utility functions for the individual states
    # within the state machine.
    
    def __init__(self):
        # displays the present state ieee of 1149.10
        
        print('Processing current state: ', str(self))
    
    def on_event(self, event):
        # handles events that are designated to this state
        
        pass
    
    def __repr__(self):
        # leverages the __str__ method to describe the state
        
        return self.__str__()
    
    def __str__(self):
        # returns the name of the state
        
        return self.__class__.__name__


class off_state(ieeestd):
    # ieee 1149.10 being in off state
    
    def __init__(self):
        ieeestd.__init__(self)
    
    def on_event(self, outer_attributes, event):
        self.outer_attributes = outer_attributes
        
        if event == 'power_on':
            # powering up the ieee 1149.10
            
            print('TAP documented in BSDL')
            
            # power-on reset (PORRESET)
            self.outer_attributes['TAP']['PORRESET'] = 1
            print('Clearing Update flop to zero')
            print('Disabling IEEE 1149.10 operation')
            
            return mission_mode(self.outer_attributes), self.outer_attributes
        else:
            print("Error: Command doesn't exist")
            return self, self.hstap_tap_pedda_outer.attributes


class system_reset(ieeestd):
    # reseting the system using system reset command
    # ieee 1149.10 shifts back to mission mode
    
    def __init__(self):
        ieeestd.__init__(self)
    
    def on_event(self, outer_attributes, event):
        self.outer_attributes = outer_attributes
        if event == 'system_reset_final':
            return mission_mode(self.outer_attributes), self.outer_attributes
        else:
            print("Error: Command doesn't exist")    
            return self, self.outer_attributes


class mission_mode(ieeestd):
    # the mission mode 
    
    def __init__(self, outer_attributes):
        # initialises all the variables to needed values

        ieeestd.__init__(self)
        self.outer_attributes = outer_attributes
        
        print('HSTAP shared with mission mode I/O interface')
        print('TAP has been detected')
        
        self.outer_attributes['TAP']['PORRESET'] = 0
        
        self.outer_attributes['HSTAP']['HSTAP_NUM'] = 1
        self.outer_attributes['HSTAP']['PEDDA_NAME'] = 'PEDDA1'
        self.outer_attributes['HSTAP']['RX_1149_10'] = [1]
        self.outer_attributes['HSTAP']['TX_1149_10'] = [1]
        self.outer_attributes['HSTAP']['COMPLIANCE_VIA_TAP'] = True
        self.outer_attributes['HSTAP']['IDLE_CHAR_REQUIRED'] = True
        self.outer_attributes['HSTAP']['ENCODING_1149_10'] = '64B_66B'
        
        self.outer_attributes['PEDDA']['PEDDA_NAME'] = 'PEDDA1'
        self.outer_attributes['PEDDA']['TARGET_ID'] = hexstr(4, hex(0))
                
        self.outer_attributes['PACKET_MAP']['PEDDA_NAME'] = 'PEDDA1'
        self.outer_attributes['PACKET_MAP']['SCAN_DATA_SIZE'] = 8
        self.outer_attributes['PACKET_MAP']['TX_ORDER'] = 'LSB_FIRST'
        self.outer_attributes['PACKET_MAP']['CMD_PARITY'] = 'NONE_1149_10'
        self.outer_attributes['PACKET_MAP']['INTERLEAVE_SIZE'] = 4
        self.outer_attributes['PACKET_MAP']['SCAN_GROUP'] = 1
        self.outer_attributes['PACKET_MAP']['PACK'] = True
        
        self.outer_attributes['CONTROL_CHAR']['SOP_CHAR'] = '0xfb'
        self.outer_attributes['CONTROL_CHAR']['EOP_CHAR'] = '0xfd'
        self.outer_attributes['CONTROL_CHAR']['IDLE_CHAR'] = '0x07'
        self.outer_attributes['CONTROL_CHAR']['ERROR_CHAR'] = '0xfe'
        self.outer_attributes['CONTROL_CHAR']['XOFF_CHAR'] = '0x7c'
        self.outer_attributes['CONTROL_CHAR']['XON_CHAR'] = '0x1c'
        self.outer_attributes['CONTROL_CHAR']['CLEAR_CHAR'] = '0x5c'
        self.outer_attributes['CONTROL_CHAR']['COMPLIANCE_CHAR'] = '0xf7'
        self.outer_attributes['CONTROL_CHAR']['BOND_CHAR'] = '0xde'
        
        self.outer_attributes['SCAN_CHANNEL_ASSOCIATION']['SCA_GROUP_0']['PEDDA_NAME'] = 'PEDDA1'
        self.outer_attributes['SCAN_CHANNEL_ASSOCIATION']['SCA_GROUP_0']['SCAN_GROUP'] = 0
        self.outer_attributes['SCAN_CHANNEL_ASSOCIATION']['SCA_GROUP_0']['DEVICE_ID'] = 'CUT1'
        for items in self.outer_attributes['SCAN_CHANNEL_ASSOCIATION']['SCA_GROUP_1']:
            self.outer_attributes['SCAN_CHANNEL_ASSOCIATION']['SCA_GROUP_1'][items] = [False, ['0']*8]
        self.outer_attributes['SCAN_CHANNEL_ASSOCIATION']['SCA_GROUP_1']['INTERNAL0'] = [False, ['0']*32]
        self.outer_attributes['SCAN_CHANNEL_ASSOCIATION']['SCA_GROUP_1']['INTERNAL3'] = [False, ['0']*33]
        self.outer_attributes['SCAN_CHANNEL_ASSOCIATION']['SCA_GROUP_1']['PEDDA_NAME'] = 'PEDDA1'
        self.outer_attributes['SCAN_CHANNEL_ASSOCIATION']['SCA_GROUP_1']['SCAN_GROUP'] = 1
        
        print('Initiliasing the attributes of MyChip: ')
        print_dict(self.outer_attributes)
        logger('Initialised Attributes: ' + str(self.outer_attributes))
        
    def on_event(self, outer_attributes, event):
        self.outer_attributes = outer_attributes
        
        if event == 'compliance_enable':
            # if compliance has to be enabled, ieee 1149.10 has two options to do it
            # one is to by receiving a compliance char from ATE
            # another is by using TAP

            if self.outer_attributes['HSTAP']['COMPLIANCE_VIA_TAP'] == 1:
                print('COMPLIANCE_VIA_TAP is True')
                print('Configuring RX_1149_10 and TX_1149_10')
            else:
                print("Compliance isn't enabled")    
                return self, self.outer_attributes

            # enables compliance by receiving compliance char
            # can't be done practically here, so just enabling it here
            print('Compliance Enable Character Received via HSTAP')
            self.outer_attributes['TAP']['COMPLIANCE_ENABLE'] = 1
            
            return compliant_mode(), self.outer_attributes

        elif event == 'power_off':
            # power off ieee 1149.10
            return off_state(), self.outer_attributes

        else:
            print("Error: Command doesn't exist")    
            return self, self.outer_attributes

    def tap_hstap(self, event):
        # excluding this as this is never being used
        # enable character is always enabled hence hstap is the one communicating to pedda
        
        pass


class compliant_mode(ieeestd):
    # defines the compliance mode of ieee 1149.10

    def __init__(self):
        ieeestd.__init__(self)
    
    def on_event(self, outer_attributes, event):
        self.outer_attributes = outer_attributes
        
        if event == 'enable_assert':
            print('Starting Enable_1149_10 PDL Procedure')
            return enable_iproc(self.outer_attributes), self.outer_attributes
        else:
            print("Error: Command doesn't exist")    
            return self, self.outer_attributes


def enable_iproc(outer_attributes):
    # following Enable_iProc steps

    outer_attributes['TAP']['ENABLE_1149_10'] = 1
    return enabled(outer_attributes)

def disable_iproc(outer_attributes):
    # following Disable_iProc steps

    outer_attributes['TAP']['ENABLE_1149_10'] = 0
    return mission_mode(outer_attributes)


class enabled(ieeestd):
    # specifies the enabled state of ieee 1149.10

    def __init__(self, outer_attributes):
        ieeestd.__init__(self)
        self.outer_attributes = outer_attributes
        # something upon attributes
        print('Feeding System Clock to Clock Control')
    
    def on_event(self, outer_attributes, event):
        self.outer_attributes = outer_attributes
        
        if event == 'power_off':
            return off_state(), self.outer_attributes
        elif event == 'system_reset':
            return system_reset(), self.outer_attributes
        elif event == 'enable_deassert':
            return disable_iproc(self.outer_attributes), self.outer_attributes
        else:
            print("Error: Command doesn't exist")    
            return self, self.outer_attributes
        
    class hstap_pedda():
        def __init__(self, outer_attributes):
            self.outer_attributes = outer_attributes
            print('Ready to receive serial bitstream')
        
        def automation(self, loaded_bitstream):
            # responsible for calling all functions and functioning of HSTAP PEDDA interface

            # loads the input bitstream. 
            # removing line char. unix has a bug of adding an invisible line break char
            self.loaded_bitstream = loaded_bitstream.rstrip("\n")
            incoming_bits = True
            output_bitstream = ''
            
            # keeps cycling until the loaded bits runs out
            while(incoming_bits):
                packet = False

                # initialising the respective objects
                hstap_component = self.hstap(self.outer_attributes)
                pedda_component = self.pedda(self.outer_attributes)
                circuit_component = self.circuit(self.outer_attributes)
                
                # looping until a particular packet transmission and receiving is completed
                while(not(packet)):
                    subpacket = False
                    
                    # receives the loaded serial bitstream bit by bit into a parallel bus
                    while(not(subpacket)):
                        bit, self.loaded_bitstream = self.receive_bitstream(self.loaded_bitstream)
                        subpacket = hstap_component.sipo(bit)
                    
                    print('Sending bitstream parallely to PEDDA: ', subpacket)

                    # decodes the packet from specified encoding method
                    packet = pedda_component.packet_decoder(subpacket)
                
                incoming_bits = bool(len(self.loaded_bitstream))

                # recognises the packet and divides into subpackets for transmission
                packet, self.outer_attributes = pedda_component.packet_command(self.outer_attributes).packet_recognizer(packet, circuit_component)
                subpackets = pedda_component.packet_encoder(packet)
                
                for i in range(len(subpackets)):
                    subpacket = subpackets[i]
                    print('Receiving bitstream parallely from PEDDA: ', subpacket)
                    
                    # transmits back the bits from parallel into serial
                    while(len(subpacket)):
                        bit, subpacket = hstap_component.piso(subpacket)
                        self.transmit_bitstream(bit)
                        output_bitstream = output_bitstream + bit
            
            return output_bitstream, self.outer_attributes
        
        def receive_bitstream(self, loaded_bitstream):
            # receives the bit from loaded bitstream

            bit = loaded_bitstream[0]
            loaded_bitstream = loaded_bitstream[1:]
            print('Receiving Bitstream Serially from ATE: ', bit)
            return bit, loaded_bitstream
            
        def transmit_bitstream(self, bit):
            # just displays that hstap is sending back bits in a serial manner

            print('Transmitting Bitstream Serially to ATE: ', bit)
            
        
        class hstap():
            # hstap subclass of hstap pedda interface
            # has all the functions that hstap must do

            def __init__(self, outer_attributes):
                self.outer_attributes = outer_attributes
                self.subpacket = ''
                
            def sipo(self, bit):
                # serial input to parallel output

                if self.outer_attributes['HSTAP']['ENCODING_1149_10'] == '64B_66B':
                    self.subpacket = self.subpacket + bit
                    if len(self.subpacket) == 66:
                        subpacket = self.subpacket
                        self.subpacket = ''
                        return subpacket
                    else:
                        return False
                elif self.outer_attributes['HSTAP']['ENCODING_1149_10'] == '8B_10B':
                    return False
                else:
                    return False
                
            def piso(self, subpacket):
                # parallel input to serial output

                if self.outer_attributes['HSTAP']['ENCODING_1149_10'] == '64B_66B':
                    bit = subpacket[0]
                    subpacket = subpacket[1:]
                    return bit, subpacket
                elif self.outer_attributes['HSTAP']['ENCODING_1149_10'] == '8B_10B':
                    return False
                else:
                    return False
                
        
        class pedda():
            # pedda subclass of hstap pedda interface
            # has all the functions that pedda must do

            def __init__(self, outer_attributes):
                self.outer_attributes = outer_attributes
                self.packet = []
                
            def packet_encoder(self, packet):
                # encodes packets into given encoding attribute

                if self.outer_attributes['HSTAP']['ENCODING_1149_10'] == '64B_66B':
                    print('Encoding from 66B to 64B')

                    # encoding for static packets
                    if packet[0] in ['0x01', '0x02', '0x03', '0x04', '0x07', '0x81', '0x82', '0x83', '0x84', '0x87']:
                        packet.insert(7, '0x87')
                        packet.insert(7, '10')
                        packet.insert(0, '0x78')
                        packet.insert(0, '10')
                        
                        reverse_flag = 0
                        if self.outer_attributes['PACKET_MAP']['TX_ORDER'] == 'LSB_FIRST':
                            reverse_flag = 1
                            
                        for i in range(1, 9):
                            packet[i] = binstr(8, bin(int(packet[i], 16)))[2:]
                            packet[i] = packet[i][::-1] if reverse_flag == 1 else packet[i]
                        packet[10] = binstr(8, bin(int(packet[10], 16)))[2:]
                        for i in range(11, len(packet)):
                            packet[i] = binstr(7, bin(int(packet[i], 16)))[2:]
                            packet[i] = packet[i][::-1] if reverse_flag == 1 else packet[i]
                        subpackets = [''.join(packet[0:9]), ''.join(packet[9:len(packet)])]
                        
                        return subpackets
                    
                    # encoding for channel select dynamic packet
                    # assumption: works only for 4 channel select words = 64 scan channels
                    elif packet[0] == '0x85':
                        channel_select = packet[4][2:] + packet[3][2:]
                        channel_select_count = int(channel_select, 16)
                        
                        reverse_flag = 0
                        if self.outer_attributes['PACKET_MAP']['TX_ORDER'] == 'LSB_FIRST':
                            reverse_flag = 1
                        
                        packet.insert(0, '0x78')
                        packet.insert(0, '10')
                        
                        if channel_select_count == 1:
                            packet.insert(9, '0xcc')
                            packet.insert(9, '10')
                            for i in range(1, 9):
                                packet[i] = binstr(8, bin(int(packet[i], 16)))[2:]
                                packet[i] = packet[i][::-1] if reverse_flag == 1 else packet[i]
                            packet[10] = binstr(8, bin(int(packet[10], 16)))[2:]
                            for i in range(11, len(packet) - 4):
                                packet[i] = binstr(8, bin(int(packet[i], 16)))[2:]
                                packet[i] = packet[i][::-1] if reverse_flag == 1 else packet[i]
                            packet[len(packet) - 4] = binstr(3, bin(int(packet[len(packet) - 4], 16)))[2:]
                            for i in range(len(packet) - 3, len(packet)):
                                packet[i] = binstr(7, bin(int(packet[i], 16)))[2:]
                                packet[i] = packet[i][::-1] if reverse_flag == 1 else packet[i]

                            subpackets = [''.join(packet[0:9]), ''.join(packet[9:len(packet)])]
                        
                        elif channel_select_count == 2 or 3:
                            packet.insert(9, '01')
                            packet.insert(18, '0x87')
                            packet.insert(18, '10')

                            for i in range(1, 9):
                                packet[i] = binstr(8, bin(int(packet[i], 16)))[2:]
                                packet[i] = packet[i][::-1] if reverse_flag == 1 else packet[i]
                            for i in range(10, 18):
                                packet[i] = binstr(8, bin(int(packet[i], 16)))[2:]
                                packet[i] = packet[i][::-1] if reverse_flag == 1 else packet[i]
                            packet[19] = binstr(8, bin(int(packet[19], 16)))[2:]
                            for i in range(20, len(packet)):
                                packet[i] = binstr(7, bin(int(packet[i], 16)))[2:]
                                packet[i] = packet[i][::-1] if reverse_flag == 1 else packet[i]
                            
                            subpackets = [''.join(packet[0:9]), ''.join(packet[9:18]), ''.join(packet[18:len(packet)])]
                                                
                        elif channel_select_count == 4:
                            packet.insert(9, '01')
                            packet.insert(18, '0xcc')
                            packet.insert(18, '10')

                            for i in range(1, 9):
                                packet[i] = binstr(8, bin(int(packet[i], 16)))[2:]
                                packet[i] = packet[i][::-1] if reverse_flag == 1 else packet[i]
                            for i in range(10, 18):
                                packet[i] = binstr(8, bin(int(packet[i], 16)))[2:]
                                packet[i] = packet[i][::-1] if reverse_flag == 1 else packet[i]
                            packet[19] = binstr(8, bin(int(packet[19], 16)))[2:]
                            for i in range(20, len(packet) - 4):
                                packet[i] = binstr(8, bin(int(packet[i], 16)))[2:]
                                packet[i] = packet[i][::-1] if reverse_flag == 1 else packet[i]
                            packet[len(packet) - 4] = binstr(3, bin(int(packet[len(packet) - 4], 16)))[2:]
                            for i in range(len(packet) - 3, len(packet)):
                                packet[i] = binstr(7, bin(int(packet[i], 16)))[2:]
                                packet[i] = packet[i][::-1] if reverse_flag == 1 else packet[i]
                            
                            subpackets = [''.join(packet[0:9]), ''.join(packet[9:18]), ''.join(packet[18:len(packet)])]
                        
                        return subpackets
                    
                    # encoding for scan dynamic packet
                    # assumption: works only for 3 payload frames
                    elif packet[0] == '0x86':
                        payload_frames = packet[6][2:] + packet[5][2:] + packet[4][2:] + packet[3][2:]
                        payload_frames_count = int(payload_frames, 16)
                        
                        reverse_flag = 0
                        if self.outer_attributes['PACKET_MAP']['TX_ORDER'] == 'LSB_FIRST':
                            reverse_flag = 1
                        
                        packet.insert(0, '0x78')
                        packet.insert(0, '10')
                        
                        if payload_frames_count == 0:
                            packet.insert(9, '01')
                            packet.insert(18, '0x87')
                            packet.insert(18, '10')

                            for i in range(1, 9):
                                packet[i] = binstr(8, bin(int(packet[i], 16)))[2:]
                                packet[i] = packet[i][::-1] if reverse_flag == 1 else packet[i]
                            for i in range(10, 18):
                                packet[i] = binstr(8, bin(int(packet[i], 16)))[2:]
                                packet[i] = packet[i][::-1] if reverse_flag == 1 else packet[i]
                            packet[19] = binstr(8, bin(int(packet[19], 16)))[2:]
                            for i in range(20, len(packet)):
                                packet[i] = binstr(7, bin(int(packet[i], 16)))[2:]
                                packet[i] = packet[i][::-1] if reverse_flag == 1 else packet[i]
                            
                            subpackets = [''.join(packet[0:9]), ''.join(packet[9:18]), ''.join(packet[18:len(packet)])]
                        
                        elif payload_frames_count == 1:
                            packet.insert(9, '01')
                            packet.insert(18, '0xcc')
                            packet.insert(18, '10')

                            for i in range(1, 9):
                                packet[i] = binstr(8, bin(int(packet[i], 16)))[2:]
                                packet[i] = packet[i][::-1] if reverse_flag == 1 else packet[i]
                            for i in range(10, 18):
                                packet[i] = binstr(8, bin(int(packet[i], 16)))[2:]
                                packet[i] = packet[i][::-1] if reverse_flag == 1 else packet[i]
                            packet[19] = binstr(8, bin(int(packet[19], 16)))[2:]
                            for i in range(20, len(packet) - 4):
                                packet[i] = binstr(8, bin(int(packet[i], 16)))[2:]
                                packet[i] = packet[i][::-1] if reverse_flag == 1 else packet[i]
                            packet[len(packet) - 4] = binstr(3, bin(int(packet[len(packet) - 4], 16)))[2:]
                            for i in range(len(packet) - 3, len(packet)):
                                packet[i] = binstr(7, bin(int(packet[i], 16)))[2:]
                                packet[i] = packet[i][::-1] if reverse_flag == 1 else packet[i]
                            
                            subpackets = [''.join(packet[0:9]), ''.join(packet[9:18]), ''.join(packet[18:len(packet)])]
                                                
                        elif payload_frames_count == 2:
                            packet.insert(9, '01')
                            packet.insert(18, '01')
                            packet.insert(27, '0x87')
                            packet.insert(27, '10')

                            for i in range(1, 9):
                                packet[i] = binstr(8, bin(int(packet[i], 16)))[2:]
                                packet[i] = packet[i][::-1] if reverse_flag == 1 else packet[i]
                            for i in range(10, 18):
                                packet[i] = binstr(8, bin(int(packet[i], 16)))[2:]
                                packet[i] = packet[i][::-1] if reverse_flag == 1 else packet[i]
                            for i in range(19, 27):
                                packet[i] = binstr(8, bin(int(packet[i], 16)))[2:]
                                packet[i] = packet[i][::-1] if reverse_flag == 1 else packet[i]
                            packet[28] = binstr(8, bin(int(packet[28], 16)))[2:]
                            for i in range(29, len(packet)):
                                packet[i] = binstr(7, bin(int(packet[i], 16)))[2:]
                                packet[i] = packet[i][::-1] if reverse_flag == 1 else packet[i]

                            subpackets = [''.join(packet[0:9]), ''.join(packet[9:18]), ''.join(packet[18:27]), ''.join(packet[27:len(packet)])]
                        
                        return subpackets
                    
                elif self.outer_attributes['HSTAP']['ENCODING_1149_10'] == '8B_10B':
                    # support for 8B/10B encoding can be added here
                    pass

                else:
                    # if neither of the encoding is specified
                    raise Exception('No Encoding is specified')
                    pass
            
            def packet_decoder(self, subpacket):
                # decoding the incoming packet using the respective encoding techniques

                if self.outer_attributes['HSTAP']['ENCODING_1149_10'] == '64B_66B':
                    # uses a subset of the original 64B/66B encoding from ieee std 802.3

                    print('Decoding from 66B to 64B')
                    
                    def reverser(merged_subpacket):
                        for i in range(1, len(merged_subpacket)):
                            merged_subpacket[i] = merged_subpacket[i][::-1]
                        return merged_subpacket
                    
                    reverse_flag = 0
                    if self.outer_attributes['PACKET_MAP']['TX_ORDER'] == 'LSB_FIRST':
                        reverse_flag = 1
                    
                    # pattern: DDDD/DDDD
                    if subpacket[0:2] == '01':
                        merged_subpacket = [subpacket[0: 2], subpacket[2: 10], subpacket[10: 18], 
                                            subpacket[18: 26], subpacket[26: 34], subpacket[34: 42], 
                                            subpacket[42: 50], subpacket[50: 58], subpacket[58: 66]]
                        self.packet.extend(reverser(merged_subpacket)) if reverse_flag == 1 else self.packet.extend(merged_subpacket)
                        return False

                    # pattern: ZZZZ/ZZZZ
                    elif subpacket[0:10] == '1001111000': 
                        merged_subpacket = [subpacket[0: 2], subpacket[2: 10], subpacket[10: 17], 
                                            subpacket[17: 24], subpacket[24: 31], subpacket[31: 38], 
                                            subpacket[38: 45], subpacket[45: 52], subpacket[52: 59], 
                                            subpacket[59: 66]]
                        self.packet.extend(reverser(merged_subpacket)) if reverse_flag == 1 else self.packet.extend(merged_subpacket)
                        return False

                    # pattern: ZZZZ/SDDD
                    elif subpacket[0:10] == '1011001100': 
                        merged_subpacket = [subpacket[0: 2], subpacket[2: 10],  subpacket[10: 17], 
                                            subpacket[17: 24], subpacket[24: 31], subpacket[31: 38], 
                                            subpacket[38: 42], subpacket[42: 50], subpacket[50, 58], 
                                            subpacket[58: 66]]
                        self.packet.extend(reverser(merged_subpacket)) if reverse_flag == 1 else self.packet.extend(merged_subpacket)
                        return False

                    # pattern: SDDD/DDDD
                    elif subpacket[0:10] == '1000011110': 
                        merged_subpacket = [subpacket[0: 2], subpacket[2: 10], subpacket[10: 18], 
                                            subpacket[18: 26], subpacket[26: 34], subpacket[34: 42], 
                                            subpacket[42: 50], subpacket[50: 58], subpacket[58: 66]]
                        self.packet.extend(reverser(merged_subpacket)) if reverse_flag == 1 else self.packet.extend(merged_subpacket)
                        return False

                    # pattern: TZZZ/ZZZZ
                    elif subpacket[0:10] == '1011100001': 
                        merged_subpacket = [subpacket[0: 2], subpacket[2: 10], subpacket[10: 17], 
                                            subpacket[17: 24], subpacket[24: 31], subpacket[31: 38], 
                                            subpacket[38: 45], subpacket[45: 52], subpacket[52: 59], 
                                            subpacket[59: 66]]
                        self.packet.extend(reverser(merged_subpacket)) if reverse_flag == 1 else self.packet.extend(merged_subpacket)
                        return self.packet

                    # pattern: DDDD/TZZZ
                    elif subpacket[0:10] == '1000110011': 
                        merged_subpacket = [subpacket[0: 2], subpacket[2: 10],  subpacket[10: 18], 
                                            subpacket[18: 26], subpacket[26: 34], subpacket[34: 42], 
                                            subpacket[42: 45], subpacket[45: 52], subpacket[52: 59], 
                                            subpacket[59: 66]]
                        self.packet.extend(reverser(merged_subpacket)) if reverse_flag == 1 else self.packet.extend(merged_subpacket)
                        return self.packet

                elif self.outer_attributes['HSTAP']['ENCODING_1149_10'] == '8B_10B':
                    # support for 8B/10B encoding can be added here
                    pass

                else:
                    # if neither of the encoding is specified
                    raise Exception('No Encoding is specified')
                    pass
            
            class packet_command():
                # class for handling commands in the packets decoded

                def __init__(self, outer_attributes):
                    self.outer_attributes = outer_attributes
                    print('Recognizing the Packet')
                
                def packet_recognizer(self, packet, circuit_component):
                    # main function for recognising the packet received

                    def crc32_checker(data_packet, crc32):
                        # checks the CRC32 for any missing/corrupted data

                        print('Checking CRC32 of data characters in the packet')
                        if hex(bn.crc32(bn.a2b_hex(data_packet))) == crc32:
                            print('CRC32 Verified')
                            return True

                        else:
                            print('CRC32 Check failed')
                            print('Data Packet:', data_packet)
                            print('CRC32 received:', crc32)
                            print('CRC32 expected:', hex(bn.crc32(bn.a2b_hex(data_packet))))
                            return False
                        
                    def crc32_coder(data_packet):
                        # returns the crc32 for the data packet being sent to hstap back from pedda
                        # which will be transmitted later to ATE
                        return hexstr(8, hex(bn.crc32(bn.a2b_hex(data_packet))))
                    
                    # switch case statement
                    switcher = {
                        '0x01': 'CONFIG',
                        '0x02': 'TARGET',
                        '0x03': 'RESET',
                        '0x04': 'RAW',
                        '0x05': 'CHSELECT',
                        '0x06': 'SCAN',
                        '0x07': 'BOND',
                    }
                    
                    def CONFIG(packet):
                        print('Received CONFIG packet')
                        logger('Received CONFIG Packet: ' + str(packet))
                        
                        data_packet = packet[0][2:] + packet[1][2:] + packet[2][2:]
                        CRC32 = packet[6] + packet[5][2:] + packet[4][2:] + packet[3][2:]
                        checked = crc32_checker(data_packet, CRC32)
                        
                        if checked:
                            self.outer_attributes['PEDDA']['TARGET_ID'] = '0x' + packet[2][2:] + packet[1][2:]
                            print('TARGET_ID of', self.outer_attributes['PEDDA']['PEDDA_NAME'], ' is now set to', self.outer_attributes['PEDDA']['TARGET_ID'])
                            logger('TARGET_ID of ' + str(self.outer_attributes['PEDDA']['PEDDA_NAME']) + ' is now set to ' +  str(self.outer_attributes['PEDDA']['TARGET_ID']))
                        else:
                            print('TARGET_ID not set')
                            packet[11] = self.outer_attributes['CONTROL_CHAR']['ERROR_CHAR']
                        
                        packet[0] = '0x81'
                        data_packet = packet[0][2:] + packet[1][2:] + packet[2][2:]
                        CRC32 = crc32_coder(data_packet)[2:]
                        packet[6] = '0x' + CRC32[:2]
                        packet[5] = '0x' + CRC32[2:4]
                        packet[4] = '0x' + CRC32[4:6]
                        packet[3] = '0x' + CRC32[6:]

                        print('Transmitting back CONFIGR packet')
                        logger('Transmitting back CONFIGR packet: ' + str(packet))
                        return packet, self.outer_attributes
                    
                    def TARGET(packet):
                        print('Received TARGET packet')
                        logger('Received TARGET Packet: ' + str(packet))
                        
                        if self.outer_attributes['PEDDA']['TARGET_ID'] == '0x0000':
                            print('TARGET_ID not set')
                            print('Forwarding back the packet')
                            return packet, self.outer_attributes
                        else:
                            data_packet = packet[0][2:] + packet[1][2:] + packet[2][2:]
                            CRC32 = packet[6] + packet[5][2:] + packet[4][2:] + packet[3][2:]
                            checked = crc32_checker(data_packet, CRC32)
                            
                            if checked:
                                print('Subsequent packets will be for the IEEE 1149.10 interface with TARGET_ID ', self.outer_attributes['PEDDA']['TARGET_ID'])
                            else:
                                packet[11] = self.outer_attributes['CONTROL_CHAR']['ERROR_CHAR']
                            
                            packet[0] = '0x82'
                            data_packet = packet[0][2:] + packet[1][2:] + packet[2][2:]
                            CRC32 = crc32_coder(data_packet)[2:]
                            packet[6] = '0x' + CRC32[:2]
                            packet[5] = '0x' + CRC32[2:4]
                            packet[4] = '0x' + CRC32[4:6]
                            packet[3] = '0x' + CRC32[6:]

                            print('Transmitting back TARGETR packet')
                            logger('Transmitting back TARGETR Packet: ' + str(packet))
                            return packet, self.outer_attributes
                    
                    def RESET(packet):
                        print('Received RESET packet')
                        logger('Received RESET Packet: ' + str(packet))
                        
                        if self.outer_attributes['PEDDA']['TARGET_ID'] == '0x0000':
                            print('TARGET_ID not set')
                            print('Forwarding back the packet')
                            return packet, self.outer_attributes
                        else:
                            data_packet = packet[0][2:] + packet[1][2:] + packet[2][2:]
                            CRC32 = packet[6] + packet[5][2:] + packet[4][2:] + packet[3][2:]
                            checked = crc32_checker(data_packet, CRC32)
                            
                            if checked:
                                if packet[1] == '0x01':
                                    print('Enabling RESET10')
                                    self.outer_attributes['PEDDA']['RESET10'] = 1
                                    logger('RESET10 is now set to ' + str(self.outer_attributes['PEDDA']['RESET10']))
                                elif packet[1] == '0x02':
                                    print('Enabling TRST10')
                                    self.outer_attributes['PEDDA']['TRST10'] = 1
                                    logger('TRST10 is now set to ' + str(self.outer_attributes['PEDDA']['TRST10']))
                                elif packet[1] == '0x00':
                                    print('Disablibg TRST10')
                                    self.outer_attributes['PEDDA']['TRST10'] = 0
                                    logger('TRST10 is now set to ' + str(self.outer_attributes['PEDDA']['TRST10']))
                                elif packet[1] == '0x04':
                                    print('Clearing TARGET_ID of ', self.outer_attributes['PEDDA']['PEDDA_NAME'])
                                    self.outer_attributes['PEDDA']['TARGET_ID'] = hexstr(4, hex(0))
                                    logger('TARGET_ID of ' + str(self.outer_attributes['PEDDA']['PEDDA_NAME']) + ' is now set to ' +  str(self.outer_attributes['PEDDA']['TARGET_ID']))
                            else:
                                packet[11] = self.outer_attributes['CONTROL_CHAR']['ERROR_CHAR']
                            
                            # deasserting reset10 left at designer's discretion
                            
                            packet[0] = '0x83'
                            data_packet = packet[0][2:] + packet[1][2:] + packet[2][2:]
                            CRC32 = crc32_coder(data_packet)[2:]
                            packet[6] = '0x' + CRC32[:2]
                            packet[5] = '0x' + CRC32[2:4]
                            packet[4] = '0x' + CRC32[4:6]
                            packet[3] = '0x' + CRC32[6:]

                            print('Transmitting back RESETR packet')
                            logger('Transmitting back RESETR Packet: ' + str(packet))
                            return packet, self.outer_attributes
                    
                    def RAW(packet):
                        print('Received RAW packet')
                        logger('Received RAW Packet: ' + str(packet))
                        
                        if self.outer_attributes['PEDDA']['TARGET_ID'] == '0x0000':
                            print('TARGET_ID not set')
                            print('Forwarding back the packet')
                            return packet, self.outer_attributes
                        else:
                            data_packet = packet[0][2:] + packet[1][2:] + packet[2][2:]
                            CRC32 = packet[6] + packet[5][2:] + packet[4][2:] + packet[3][2:]
                            checked = crc32_checker(data_packet, CRC32)
                            
                            if checked:
                                print('Enabling loopback mode')
                                self.outer_attributes['PEDDA']['RAWMODE_1149_10'] = 1
                                logger('RAWMODE is now set to ' + str(self.outer_attributes['PEDDA']['RAWMODE_1149_10']))
                            else:
                                packet[11] = self.outer_attributes['CONTROL_CHAR']['ERROR_CHAR']
                            
                            packet[0] = '0x84'
                            data_packet = packet[0][2:] + packet[1][2:] + packet[2][2:]
                            CRC32 = crc32_coder(data_packet)[2:]
                            packet[6] = '0x' + CRC32[:2]
                            packet[5] = '0x' + CRC32[2:4]
                            packet[4] = '0x' + CRC32[4:6]
                            packet[3] = '0x' + CRC32[6:]

                            print('Transmitting back RAWR packet')
                            logger('Transmitting back RAWR Packet: ' + str(packet))
                            return packet, self.outer_attributes
                    
                    def CHSELECT(packet):
                        print('Received CH-SELECT packet')
                        logger('Received CH-SELECT Packet: ' + str(packet))
                        
                        if self.outer_attributes['PEDDA']['TARGET_ID'] == '0x0000':
                            print('TARGET_ID not set')
                            print('Forwarding back the packet')
                            return packet, self.outer_attributes
                        
                        else:
                            self.outer_attributes['PACKET_MAP']['SCAN_GROUP'] = 0
                            scan_group = packet[2][2:] + packet[1][2:]
                            scan_group_target = int(scan_group, 16)
                            channel_select = packet[4][2:] + packet[3][2:]
                            channel_select_count = int(channel_select, 16)
                            print('Targeting Scan Group', scan_group_target, 'in', channel_select_count, 'scan groups')
                            
                            merged_channel_select = ''
                            merged_channel_select_data = ''
                            for i in range(2*channel_select_count):
                                merged_channel_select = merged_channel_select + packet[4 + 2*channel_select_count - i][2:]
                                merged_channel_select_data = merged_channel_select_data + packet[5 + i][2:]
                            zero_byte_count = 2 * ((channel_select_count - 1) % 2)
                            merged_zero_bytes = ''
                            for i in range(zero_byte_count):
                                merged_zero_bytes = merged_zero_bytes + packet[5 + (2*channel_select_count) + i][2:]
                            
                            data_packet = packet[0][2:] + packet[1][2:] + packet[2][2:] + packet[3][2:] + packet[4][2:] + merged_channel_select_data + merged_zero_bytes
                            length_of_data_packet_bytes = len(data_packet) // 2
                            CRC32 = packet[length_of_data_packet_bytes + 3] + packet[length_of_data_packet_bytes + 2][2:] + packet[length_of_data_packet_bytes + 1][2:] + packet[length_of_data_packet_bytes][2:]
                            checked = crc32_checker(data_packet, CRC32)
                            merged_channel_select = binstr(8*len(merged_channel_select), bin(int(merged_channel_select, 16)))
                            merged_channel_select = merged_channel_select[::-1]
                            
                            if checked:
                                self.outer_attributes['PACKET_MAP']['SCAN_GROUP'] = scan_group_target
                                for channel_select_word in range(channel_select_count):
                                    if (channel_select_word + 1) == scan_group_target:
                                        merged_channel_select = merged_channel_select[16*(scan_group_target - 1): 16*scan_group_target]
                                        for _ in range(merged_channel_select.count('1')):
                                            scan_channel = merged_channel_select.index('1')
                                            print('Enabling Scan Channel ', scan_channel, ' in ', scan_group_target, ' Scan Group')
                                            self.outer_attributes['SCAN_CHANNEL_ASSOCIATION']['SCA_GROUP_' + str(scan_group_target)]['INTERNAL' + str(scan_channel)][0] = True
                                            merged_channel_select = merged_channel_select.replace('1', '0', 1)
                            else:
                                try:
                                    packet[15 + 2*channel_select_count + zero_byte_count] = self.outer_attributes['CONTROL_CHAR']['ERROR_CHAR']
                                except IndexError:
                                    packet.append(self.outer_attributes['CONTROL_CHAR']['ERROR_CHAR'])
                                    packet.extend([self.outer_attributes['CONTROL_CHAR']['IDLE_CHAR'] for _ in range(7)])
                            
                            packet[0] = '0x85'
                            data_packet = packet[0][2:] + packet[1][2:] + packet[2][2:] + packet[3][2:] + packet[4][2:] + merged_channel_select_data + merged_zero_bytes
                            CRC32 = crc32_coder(data_packet)[2:]
                            packet[length_of_data_packet_bytes + 3] = '0x' + CRC32[:2]
                            packet[length_of_data_packet_bytes + 2] = '0x' + CRC32[2:4]
                            packet[length_of_data_packet_bytes + 1] = '0x' + CRC32[4:6]
                            packet[length_of_data_packet_bytes] = '0x' + CRC32[6:]
                            
                            print('Transmitting back CH-SELECTR packet')
                            logger('Transmitting back CH-SELECTR Packet: ' + str(packet))
                            return packet, self.outer_attributes
                    
                    def SCAN(packet, circuit_component):
                        print('Received SCAN packet')
                        logger('Received SCAN Packet: ' + str(packet))
                        
                        if self.outer_attributes['PEDDA']['TARGET_ID'] == '0x0000':
                            print('TARGET_ID not set')
                            print('Forwarding back the packet')
                            return packet, self.outer_attributes

                        else:
                            ID = packet[1]
                            print('SCAN Packet ID: ', int(ID, 16))
                            ICSU = binstr(8, bin(int(packet[2], 16)))[6:]
                            payload_frames = packet[6][2:] + packet[5][2:] + packet[4][2:] + packet[3][2:]
                            payload_frames_count = int(payload_frames, 16)
                            cycle = packet[10][2:] + packet[9][2:] + packet[8][2:] + packet[7][2:]
                            cycle_count = int(cycle, 16)
                            payload_data = ''
                            payload = []
                            
                            for i in range(4*payload_frames_count):
                                payload_data = payload_data + packet[11 + i][2:]
                                payload.append(packet[10 + 4*payload_frames_count - i][2:])
                            payload = ''.join([binstr(8, bin(int(payload[i], 16)))[2:][::-1] for i in range(payload_frames_count*4)])
                            
                            data_packet = packet[0][2:] + packet[1][2:] + packet[2][2:] + packet[3][2:] + packet[4][2:] + packet[5][2:] + packet[6][2:] + packet[7][2:] + packet[8][2:] + packet[9][2:] + packet[10][2:] + payload_data
                            length_of_data_packet_bytes = len(data_packet) // 2
                            CRC32 = packet[length_of_data_packet_bytes + 3] + packet[length_of_data_packet_bytes + 2][2:] + packet[length_of_data_packet_bytes + 1][2:] + packet[length_of_data_packet_bytes][2:]
                            checked = crc32_checker(data_packet, CRC32)
                            
                            if checked:
                                scan_group_target = self.outer_attributes['PACKET_MAP']['SCAN_GROUP']
                                if scan_group_target > 0:
                                    if int(ICSU, 2) != 0:
                                        self.outer_attributes['SCAN_CHANNEL_ASSOCIATION']['SCA_GROUP_0']['INSTRUCTION_REGISTER']['INSTRUCTION'] = 1 if ICSU[0] == '1' else 0
                                        self.outer_attributes['SCAN_CHANNEL_ASSOCIATION']['SCA_GROUP_0']['INSTRUCTION_REGISTER']['CAPTURE'] = 1 if ICSU[1] == '1' else 0
                                        self.outer_attributes['SCAN_CHANNEL_ASSOCIATION']['SCA_GROUP_0']['INSTRUCTION_REGISTER']['SHIFT'] = 1 if ICSU[2] == '1' else 0
                                        self.outer_attributes['SCAN_CHANNEL_ASSOCIATION']['SCA_GROUP_0']['INSTRUCTION_REGISTER']['UPDATE'] = 1 if ICSU[3] == '1' else 0
                                        
                                        interleave = self.outer_attributes['PACKET_MAP']['INTERLEAVE_SIZE']
                                        
                                        if ICSU[2] == '1':
                                            print('Shift operation being performed')
                                            for _ in range(0, cycle_count//interleave):
                                                for scan_channel in reversed(range(len(self.outer_attributes['SCAN_CHANNEL_ASSOCIATION']['SCA_GROUP_' + str(scan_group_target)]) - 2)):
                                                    if self.outer_attributes['SCAN_CHANNEL_ASSOCIATION']['SCA_GROUP_' + str(scan_group_target)]['INTERNAL' + str(scan_channel)][0] == True:
                                                        for _ in range(interleave):
                                                            scan_in = payload[0]
                                                            payload = payload[1:] + payload[:1]
                                                            temp = self.outer_attributes['SCAN_CHANNEL_ASSOCIATION']['SCA_GROUP_' + str(scan_group_target)]['INTERNAL' + str(scan_channel)][1][:-1]
                                                            temp.insert(0, scan_in)
                                                            self.outer_attributes['SCAN_CHANNEL_ASSOCIATION']['SCA_GROUP_' + str(scan_group_target)]['INTERNAL' + str(scan_channel)][1] = temp
                                            
                                            circuit_component.__init__(self.outer_attributes)
                                            self.outer_attributes = circuit_component.shift()
                                        
                                        if ICSU[1] == '1':
                                            print('Capture operation being performed')
                                            circuit_component.__init__(self.outer_attributes)
                                            self.outer_attributes = circuit_component.capture()
                                        
                                        if ICSU[3] == '1':
                                            print('Update operation being performed')
                                            circuit_component.__init__(self.outer_attributes)
                                            self.outer_attributes = circuit_component.update()
                                            
                                        payload = list(payload)
                                        for _ in range(0, cycle_count//interleave):
                                            for scan_channel in range(len(self.outer_attributes['SCAN_CHANNEL_ASSOCIATION']['SCA_GROUP_' + str(scan_group_target)]) - 2):
                                                if self.outer_attributes['SCAN_CHANNEL_ASSOCIATION']['SCA_GROUP_' + str(scan_group_target)]['INTERNAL' + str(scan_channel)][0] == True:
                                                    for _ in range(interleave):
                                                        scan_in = self.outer_attributes['SCAN_CHANNEL_ASSOCIATION']['SCA_GROUP_' + str(scan_group_target)]['INTERNAL' + str(scan_channel)][1][0]
                                                        self.outer_attributes['SCAN_CHANNEL_ASSOCIATION']['SCA_GROUP_' + str(scan_group_target)]['INTERNAL' + str(scan_channel)][1] = self.outer_attributes['SCAN_CHANNEL_ASSOCIATION']['SCA_GROUP_' + str(scan_group_target)]['INTERNAL' + str(scan_channel)][1][1:] + self.outer_attributes['SCAN_CHANNEL_ASSOCIATION']['SCA_GROUP_' + str(scan_group_target)]['INTERNAL' + str(scan_channel)][1][:1]
                                                        payload[0] = scan_in
                                                        payload = payload[-1:] + payload[:-1]
                                        
                                        payload = payload[1:] + payload[:1]
                                        payload = ''.join(list(payload))
                                    
                                    else:
                                        print('No operation will be performed as ICSU is unspecified')
                                
                                else:
                                    print('No CHSELECT Packet Received before SCAN Packet')
                                
                                payload = payload[::-1]
                                payload = [hexstr(2, hex(int(payload[i:i + 8], 2))) for i in range(0, len(payload), 8)]
                                
                                for i in range(4*payload_frames_count):
                                    packet[11 + i] = payload[i]
                            
                            else:
                                try:
                                    packet[19 + 4*payload_frames_count] = self.outer_attributes['CONTROL_CHAR']['ERROR_CHAR']
                                except IndexError:
                                    packet.append(self.outer_attributes['CONTROL_CHAR']['ERROR_CHAR'])
                                    packet.extend([self.outer_attributes['CONTROL_CHAR']['IDLE_CHAR'] for _ in range(7)])
                            
                            self.outer_attributes['PACKET_MAP']['SCAN_GROUP'] = 0
                            
                            packet[0] = '0x86'
                            data_packet = packet[0][2:] + packet[1][2:] + packet[2][2:] + packet[3][2:] + packet[4][2:] + packet[5][2:] + packet[6][2:] + packet[7][2:] + packet[8][2:] + packet[9][2:] + packet[10][2:] + payload_data
                            CRC32 = crc32_coder(data_packet)[2:]
                            packet[length_of_data_packet_bytes + 3] = '0x' + CRC32[:2]
                            packet[length_of_data_packet_bytes + 2] = '0x' + CRC32[2:4]
                            packet[length_of_data_packet_bytes + 1] = '0x' + CRC32[4:6]
                            packet[length_of_data_packet_bytes] = '0x' + CRC32[6:]
                            
                            print('Transmitting back SCANR packet')
                            logger('Transmitting back SCANR Packet: ' + str(packet))
                            return packet, self.outer_attributes
                    
                    def BOND(packet):
                        # not required as only one lane
                        
                        print('Received BOND packet')
                        logger('Received BOND Packet: ' + str(packet))
                        print('Only one lane detected')
                        
                        if self.outer_attributes['PEDDA']['TARGET_ID'] == '0x0000':
                            print('TARGET_ID not set')
                            print('Forwarding back the packet')
                            return packet, self.outer_attributes
                        
                        else:
                            data_packet = packet[0][2:] + packet[1][2:] + packet[2][2:]
                            CRC32 = packet[6] + packet[5][2:] + packet[4][2:] + packet[3][2:]
                            checked = crc32_checker(data_packet, CRC32)
                            
                            if checked:
                                pass
                            else:
                                packet[11] = self.outer_attributes['CONTROL_CHAR']['ERROR_CHAR']
                            
                            packet[0] = '0x87'
                            print('Transmitting back BONDR packet')
                            logger('Transmitting back BONDR Packet: ' + str(packet))
                            return packet, self.outer_attributes
                    
                    # removing the prefixes off the packet
                    while '10' in packet: 
                        ind = packet.index('10')
                        packet.remove('10')
                        packet.pop(ind)
                    while '01' in packet:
                        packet.remove('01')
                    
                    # converting the packets into hex
                    for ind in range(len(packet)):
                        packet[ind] = hexstr(2, hex(int(packet[ind], 2)))
                    
                    if self.outer_attributes['PEDDA']['RAWMODE_1149_10'] == 1:
                        print('RAWMODE Active: any data received is sent back as it is')
                        rawmode_condition = input('Exit RAWMODE? (Y/N): ')
                        if rawmode_condition == 'Y' or rawmode_condition == 'y':
                            print('Sending Power-On Reset Signal to disable RAWMODE')
                            self.outer_attributes['TAP']['PORRESET'] = 1
                            self.outer_attributes['PEDDA']['RAWMODE_1149_10'] = 0
                            logger('RAWMODE is now set to ' + str(self.outer_attributes['PEDDA']['RAWMODE_1149_10']))
                            self.outer_attributes['TAP']['PORRESET'] = 0
                        return packet, self.outer_attributes
                    
                    else:
                        if packet[0] in switcher:
                            command = switcher[packet[0]]
                            if command == 'SCAN':
                                return eval(command + '(packet, circuit_component)')
                            else:
                                return eval(command + '(packet)')
                        else:
                            print('Invalid CMD')
        
        class circuit():
            # circuit under test
            # assumption: any operation returns back the same attributes
            # logging can also be done inside functions as they represent after the operation has been taken place
            # as we are returing back the same attributes, so it doesn't matter

            def __init__(self, outer_attributes):
                self.outer_attributes = outer_attributes
            
            def capture(self):
                logger('SCAN Channel Association during capture operation: ' + str(self.outer_attributes['SCAN_CHANNEL_ASSOCIATION']))
                return self.outer_attributes
            
            def shift(self):
                logger('SCAN Channel Association during shift operation: ' + str(self.outer_attributes['SCAN_CHANNEL_ASSOCIATION']))
                return self.outer_attributes
            
            def update(self):
                logger('SCAN Channel Association during update operation: ' + str(self.outer_attributes['SCAN_CHANNEL_ASSOCIATION']))
                return self.outer_attributes
                    

class hstap_tap_pedda(object):
    def __init__(self):
        print('Initialising IEEE 1149.10')
        print('Starting Compliance Verification')
        
        TAP = {
            'COMPLIANCE_ENABLE': 0,
            'ENABLE_1149_10': 0,
            'TCK': 0,
            'TDI': 0,
            'TDO': 0,
            'TRST': 0,
            'SELECT_TAP': 0,
            'CAPTURE_TAP': 0,
            'SHIFT_TAP': 0,
            'UPDATE_TAP': 0,
            'RESET': 0,
            'PORRESET': 0
        }
        
        HSTAP = {
            'HSTAP_NUM': 0,
            'PEDDA_NAME': 0,
            'TX_1149_10': [0, 0],
            'RX_1149_10': [0, 0],
            'ENCODING_1149_10': 0,
            'DATARATE_1149_10': 0,
            'COMPLIANCE_VIA_TAP': 0,
            'IDLE_CHAR_REQUIRED': 0,
            'MAX_FRAMES_1149_10': 0,
            'LATENCY_1149_10': 0,
            'TXCLOCK_1149_10': 0,
            'RXCLOCK_1149_10': 0,
            'REFCLOCK_1149_10': 0,
            'SYSCLOCK_1149_10': 0,
            'SELECT_1149_10': 0,
            'BOND_1149_10': 0,
        }
        
        PEDDA = {
            'PEDDA_NAME': 0,
            'TARGET_ID': 0,
            'RAWMODE_1149_10': 0,
            'RESET10': 0,
            'TRST10': 0
            }
        
        PACKET_MAP = {
            'PEDDA_NAME': 0,
            'SCAN_DATA_SIZE': 0,
            'TX_ORDER': 0,
            'CMD_PARITY': 0,
            'INTERLEAVE_SIZE': 0,
            'SCAN_GROUP': 0,
            'PACK': 0
        }
        
        CONTROL_CHAR = {
            'SOP_CHAR': 0,
            'EOP_CHAR': 0,
            'IDLE_CHAR': 0,
            'ERROR_CHAR': 0,
            'XOFF_CHAR': 0,
            'XON_CHAR': 0,
            'CLEAR_CHAR': 0,
            'COMPLIANCE_CHAR': 0,
            'BOND_CHAR': 0
        }
        
        INSTRUCTION_REGISTER = {
            'INSTRUCTION': 0,
            'CAPTURE': 0,
            'SHIFT': 0,
            'UPDATE': 0
            }
        
        SCA_GROUP_0 = {
            'PEDDA_NAME': 0,
            'SCAN_GROUP': 0,
            'INSTRUCTION_REGISTER': INSTRUCTION_REGISTER,
            'BYPASS_REGISTER': 0,
            'BOUNDARY_SCAN_REGISTER': 0,
            'DEVICE_ID': 0,
            }
          
        SCA_GROUP_1 = {
            'PEDDA_NAME': 0,
            'SCAN_GROUP': 0,
            'INTERNAL0': 0,
            'INTERNAL1': 0,
            'INTERNAL2': 0,
            'INTERNAL3': 0,
            'INTERNAL4': 0,
            'INTERNAL5': 0,
            'INTERNAL6': 0,
            'INTERNAL7': 0,
            'INTERNAL8': 0,
            'INTERNAL9': 0,
            'INTERNAL10': 0,
            'INTERNAL11': 0,
            'INTERNAL12': 0,
            'INTERNAL13': 0,
            'INTERNAL14': 0,
            'INTERNAL15': 0
            }
        
        SCAN_CHANNEL_ASSOCIATION = {
            'SCA_GROUP_0': SCA_GROUP_0,
            'SCA_GROUP_1': SCA_GROUP_1
            }
        
        self.attributes = {
            'TAP': TAP,
            'HSTAP': HSTAP,
            'PEDDA': PEDDA,
            'PACKET_MAP': PACKET_MAP,
            'CONTROL_CHAR': CONTROL_CHAR,
            'SCAN_CHANNEL_ASSOCIATION': SCAN_CHANNEL_ASSOCIATION
            }
        
        self.state = off_state()
        
    def on_event(self, event):
        self.state, self.attributes = self.state.on_event(self.attributes, event)


def main():
    # main driver code
    
    # initiating log file
    open('output.log', 'w').close()
    logger('Log file for IEEE Std 1149.10-2017 emulation by Python')
    
    # initialises the interfce class
    device = hstap_tap_pedda()

    # powers up the interface
    logger('IEEE Std 1149.10-2017 powered on to mission mode')
    device.on_event('power_on')
        
    # enables the compliance
    device.on_event('compliance_enable')

    # asserts enable_1149_10
    logger('IEEE Std 1149.10-2017: HSTAP and PEDDA Enabled')
    device.on_event('enable_assert')
        
    # reads and loads the serial bitstream from a file
    loaded_bitstream = read_file('data_in.txt')
    
    # calls the automation function which is responsible for calling all other functions on its own
    # returns an output bitstream and updated attributes
    output_bitstream, device.attributes = device.state.hstap_pedda(device.attributes).automation(loaded_bitstream)

    # writes the output bitstream to a file
    write_file('data_out.txt', output_bitstream)

    # resets the interface
    logger('IEEE Std 1149.10-2017 reset')
    device.on_event('system_reset')
    device.on_event('system_reset_final')

    # powering off the device
    logger('IEEE Std 1149.10-2017 powered off')
    device.on_event('power_off')


if __name__ == '__main__':
    main()
