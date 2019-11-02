#THIS FILE IS AUTO GENERATED FROM THE TEMPLATE! DO NOT CHANGE!
SET(CMAKE_SYSTEM_NAME Generic)
SET(CMAKE_SYSTEM_VERSION 1)
cmake_minimum_required(VERSION 3.7)

# specify cross compilers and tools
SET(CMAKE_C_COMPILER_WORKS 1)
SET(CMAKE_C_COMPILER /Users/seva/Library/Arduino15/packages/STM32/tools/arm-none-eabi-gcc/8.2.1-1.7/bin//arm-none-eabi-gcc)
SET(CMAKE_CXX_COMPILER_WORKS 1)
SET(CMAKE_CXX_COMPILER /Users/seva/Library/Arduino15/packages/STM32/tools/arm-none-eabi-gcc/8.2.1-1.7/bin//arm-none-eabi-g++)
set(CMAKE_ASM_COMPILER  /Users/seva/Library/Arduino15/packages/STM32/tools/arm-none-eabi-gcc/8.2.1-1.7/bin//arm-none-eabi-gcc)
set(CMAKE_AR /Users/seva/Library/Arduino15/packages/STM32/tools/arm-none-eabi-gcc/8.2.1-1.7/bin//arm-none-eabi-ar)
set(CMAKE_OBJCOPY /Users/seva/Library/Arduino15/packages/STM32/tools/arm-none-eabi-gcc/8.2.1-1.7/bin//arm-none-eabi-objcopy)
set(CMAKE_OBJDUMP /Users/seva/Library/Arduino15/packages/STM32/tools/arm-none-eabi-gcc/8.2.1-1.7/bin//arm-none-eabi-objdump)
set(SIZE /Users/seva/Library/Arduino15/packages/STM32/tools/arm-none-eabi-gcc/8.2.1-1.7/bin//arm-none-eabi-size)

SET(LINKER_SCRIPT ${CMAKE_SOURCE_DIR}/STM32F103C8Tx_FLASH.ld)

#Uncomment for hardware floating point
#SET(FPU_FLAGS "-mfloat-abi=hard -mfpu=fpv4-sp-d16")
#add_definitions(-DARM_MATH_CM4 -DARM_MATH_MATRIX_CHECK -DARM_MATH_ROUNDING -D__FPU_PRESENT=1)

#Uncomment for software floating point
#SET(FPU_FLAGS "-mfloat-abi=soft")

SET(COMMON_FLAGS
    "-mcpu=cortex-m3 ${FPU_FLAGS} -mthumb -mthumb-interwork -ffunction-sections -fdata-sections \
    -g -fno-common -fmessage-length=0 -specs=nosys.specs -specs=nano.specs")

SET(CMAKE_CXX_FLAGS_INIT "${COMMON_FLAGS} -std=c++11")
SET(CMAKE_C_FLAGS_INIT "${COMMON_FLAGS} -std=gnu99")
SET(CMAKE_EXE_LINKER_FLAGS_INIT "-Wl,-gc-sections,--print-memory-usage -T ${LINKER_SCRIPT}")

PROJECT(stm_thermo C CXX ASM)
set(CMAKE_CXX_STANDARD 11)

#add_definitions(-DARM_MATH_CM4 -DARM_MATH_MATRIX_CHECK -DARM_MATH_ROUNDING -D__FPU_PRESENT=1)
add_definitions(-D__weak=__attribute__\(\(weak\)\) -D__packed=__attribute__\(\(__packed__\)\) -DUSE_HAL_DRIVER -DSTM32F103xB)

set(SOURCES Src/main.c Src/freertos.c Src/stm32f1xx_it.c Src/stm32f1xx_hal_msp.c Src/stm32f1xx_hal_timebase_tim.c Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_gpio_ex.c Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_adc.c Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_adc_ex.c Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_spi.c Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_tim.c Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_tim_ex.c Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_uart.c Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal.c Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_rcc.c Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_rcc_ex.c Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_gpio.c Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_dma.c Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_cortex.c Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_pwr.c Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_flash.c Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_flash_ex.c Drivers/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_exti.c Src/system_stm32f1xx.c Middlewares/Third_Party/FreeRTOS/Source/croutine.c Middlewares/Third_Party/FreeRTOS/Source/event_groups.c Middlewares/Third_Party/FreeRTOS/Source/list.c Middlewares/Third_Party/FreeRTOS/Source/queue.c Middlewares/Third_Party/FreeRTOS/Source/stream_buffer.c Middlewares/Third_Party/FreeRTOS/Source/tasks.c Middlewares/Third_Party/FreeRTOS/Source/timers.c Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS/cmsis_os.c Middlewares/Third_Party/FreeRTOS/Source/portable/MemMang/heap_4.c Middlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM3/port.c code/task_blink.c code/cmdline.c code/commands.c startup_stm32f103xb.s)

include_directories(Inc Drivers/STM32F1xx_HAL_Driver/Inc Drivers/STM32F1xx_HAL_Driver/Inc/Legacy Middlewares/Third_Party/FreeRTOS/Source/include Middlewares/Third_Party/FreeRTOS/Source/CMSIS_RTOS Middlewares/Third_Party/FreeRTOS/Source/portable/GCC/ARM_CM3 Drivers/CMSIS/Device/ST/STM32F1xx/Include Drivers/CMSIS/Include code)

add_executable(${PROJECT_NAME}.elf ${SOURCES} ${LINKER_SCRIPT})

set(CMAKE_EXE_LINKER_FLAGS
    "${CMAKE_EXE_LINKER_FLAGS} -Wl,-Map=${PROJECT_BINARY_DIR}/${PROJECT_NAME}.map")

set(HEX_FILE ${PROJECT_BINARY_DIR}/${PROJECT_NAME}.hex)
set(BIN_FILE ${PROJECT_BINARY_DIR}/${PROJECT_NAME}.bin)

add_custom_command(TARGET ${PROJECT_NAME}.elf POST_BUILD
        COMMAND ${CMAKE_OBJCOPY} -Oihex $<TARGET_FILE:${PROJECT_NAME}.elf> ${HEX_FILE}
        COMMAND ${CMAKE_OBJCOPY} -Obinary $<TARGET_FILE:${PROJECT_NAME}.elf> ${BIN_FILE}
        COMMENT "Building ${HEX_FILE}
Building ${BIN_FILE}")
