//
// Created by Vsevolod Lobko on 02.11.2019.
//

#ifndef STM_THERMO_TASK_THERMO_H
#define STM_THERMO_TASK_THERMO_H

extern volatile int32_t pid_targets[3];
extern volatile double pid_integrals[3];
extern volatile int32_t pid_k_i[3];
extern volatile int32_t pid_k_p[3];

extern volatile int32_t k_type_temp;
extern volatile int32_t adc_reads[5];
extern volatile int32_t ext_values[3];
extern volatile int32_t fan_values[3];
extern volatile int32_t adc_temps[3];
extern volatile int32_t heatbed_value;

void sepFunction(void);
void sfpFunction(void);
void sevFunction(void);
void sfvFunction(void);
void sptFunction(void);
void sppFunction(void);
void shpidFunction(void);

#endif  // STM_THERMO_TASK_THERMO_H
