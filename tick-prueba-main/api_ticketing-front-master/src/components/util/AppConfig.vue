<template>
    <div class="text-center">
        <v-dialog v-model="dialog" width="500">
            <template v-slot:activator="{ on, attrs }">
                <v-btn color="red lighten-2" dark v-bind="attrs" v-on="on" @click="execute()">
                    Configurar Sistema
                </v-btn>
            </template>

            <v-card>
                <v-card-title class="text-h5 grey lighten-2">
                    Seleccione sistema que usará
                </v-card-title>

                <v-card-text>
                    <v-col class="d-flex" cols="12" sm="6">
                        <v-select v-model="sistema1" :items="items" item-value="id" return-object
                            label="Sistema" />
                    </v-col>
                </v-card-text>

                <v-divider></v-divider>

                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" text @click="sendEdit()">
                        Aceptar
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>

<script lang="ts">

import { Vue, Component } from 'vue-property-decorator';
import { internet } from '@/utils/Internet';
import Util from '@/utils/Util';
import axios from "axios";

@Component({
    name: 'ConfigView'
})

export default class viewConfig {

    public validator = "Objeto no encontrado";
    public isLoading = true;
    public sistema1 = "";
    public dialogUpdate = false;
    public items = ['Zendesk', 'Freshdesk'];
    public dialog = false;

    
    public sendEdit() {
        let dt = JSON.stringify({
            'sistemaCliente': this.sistema1,
            'Cliente': 'usuario1'
        })
        console.log(dt)
        let config = {
            method: 'post',
            url: 'http://127.0.0.1:9090/config',
            data: dt,
            headers: {
                Authorization: 'Basic ' + btoa('usuario1' + ':' + 'usuario1'), "Content-Type": "application/json", "Accept": "*/*"
            }
        };
        axios(config)
            .then(response => {
                this.dialogUpdate = false;
            })
    }

    
    public execute(){
        
        this.isLoading = true;
        let config = {
            method: 'get',
            url: 'http://127.0.0.1:9090/config',
            headers: { Authorization: 'Basic ' + btoa('usuario1' + ':' + 'usuario1'), "Content-Type": "application/json", "Accept": "*/*" },
        };
        let response = axios.request(config)

        if (config.url == this.validator){
            this.aggregateItem();
        }
        else{
            console.log("pass")
        }
        }
    

    public async aggregateItem() {

        let bodyContent = JSON.stringify({ "sistemaCliente": 'Zendesk', "Cliente": 'usuario1' })
        let config = {
            method: 'put',
            url: 'http://127.0.0.1:9090/config',
            data: bodyContent,
            headers: { Authorization: 'Basic ' + btoa('usuario1' + ':' + 'usuario1'), "Content-Type": "application/json", "Accept": "*/*" }

        };
        let response = await axios.request(config)
    }

    // public getData() {
    //     this.isLoading = true;
    //     let config = {
    //         method: 'get',
    //         url: 'http://127.0.0.1:9090/config',
    //         headers: { Authorization: 'Basic ' + btoa('usuario1' + ':' + 'usuario1'), "Content-Type": "application/json", "Accept": "*/*" },
    //     };
    //     let response = axios.request(config)
    // }
}
</script>