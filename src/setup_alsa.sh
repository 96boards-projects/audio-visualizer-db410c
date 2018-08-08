#!/bin/bash

#configure left channel
amixer cset iface=MIXER,name='DEC1 MUX' 'ADC1'
amixer cset iface=MIXER,name='ADC1 Volume' 100

#configure right channel
amixer cset iface=MIXER,name='DEC2 MUX' 'ADC2'
amixer cset iface=MIXER,name='ADC2 Volume' 100
amixer cset iface=MIXER,name='ADC2 MUX' 'INP2'

