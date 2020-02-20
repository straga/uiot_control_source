#  uIOT Control - Source
#  python - PC / micropython - ESP32
## Core

> _board

_platform_ - Унификазия для PC/ESP32 работы со стримом. \
_u_os_ - Унификазия для PC/ESP32 работы со os.


> asyn

_asyn_ - дополнения для работы с asynio. \


> config - json

_config_ - манипуляция конфигурациями. \
_jason_store_ - манипуляция json файлам. \


> loader

_board_mod_ - схема для модулей \
_loader_ - загрущек для модулей из папки **mod**


> mbus

_mbus_ - шина обмена сообщениями Subscrib/Publish \

> thread

_thread_ - возможность запускать задачи asynio в другом потоке \

## lib
Библиотеки для работы - uIOT Control.

## mod
Модули - uIOT Control.

## platform
Внешнии библиотеки и зависимости.

## tools
gen_tool - генерация екземляра проекта для устройства из gen файла.



# Modules

## FTP - asyncio in thread PC/ESP32

> Конфиг хранится в json.

> Запускаем FTP.

>FTP создает ECHO CMD сервер. -> Получив команды создает объек для общения. 
>Начинается обмен командами.

>Если требуется получить/передать данные. Запускаетcя ECHO DATA.
>Региструем обращения и отвечает.



## Telnet - asyncio in thread ESP32

> Конфиг хранится в json.

## Net - PC эмуляция esp32 - network/ ESP32

> Конфиг хранится в json.