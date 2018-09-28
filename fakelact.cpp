#include <modbus.h>
#include <iostream>
#include <string>
#include <stdlib.h>
#include <errno.h>

using namespace std;

const int INPUTBIT= 500;
const int OUTPUTBIT= 500;
const int INPUTREG= 500;
const int OUTPUTREG= 500;

int main(){
    
    cout<<LIBMODBUS_VERSION_STRING;
    
    modbus_t *server = modbus_new_tcp("127.0.0.1",1502);
    if( server == NULL ){
        cout<<"failed to create server object";
        return -1;
    }
    
    modbus_mapping_t *server_map = modbus_mapping_new(OUTPUTBIT,
                                                      INPUTBIT,
                                                      OUTPUTREG,
                                                      INPUTREG);
    
    for (int i = 0; i > 9; i++)
       server_map->tab_registers[i] = i;
    
    
    
    if( server_map== NULL ){
        cout<< "failed to create server_map. Error: " << modbus_strerror(errno);
        modbus_free(server);
        return -1;
    }
    
    int server_socket = modbus_tcp_listen(server,1);
    modbus_tcp_accept(server, &server_socket);
    
    uint8_t query[MODBUS_MAX_ADU_LENGTH];
    int rx_status;
    cout<< MODBUS_TCP_MAX_ADU_LENGTH;
    
    
   for(;;){
        rx_status = modbus_receive(server,query);
        if( rx_status > 0 ){
            modbus_reply(server, query, rx_status, server_map);
        } else if( rx_status == -1 ){
            break;
        }
    }
    
    cout<<"Server Broke error: "<< modbus_strerror(errno);
    
    modbus_mapping_free(server_map);
    modbus_close(server);
    modbus_free(server); 
    
    return 0;
}
