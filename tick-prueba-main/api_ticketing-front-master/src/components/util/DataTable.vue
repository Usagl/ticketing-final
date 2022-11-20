<template>
    <div>
        <v-card-title primary-title>
            Registro Ticketing
        </v-card-title>
        <v-row justify="center">
            <v-dialog v-model="dialog" persistent max-width="600px">
                <template v-slot:activator="{ on, attrs }">
                    <v-btn color="lime" dark v-bind="attrs" v-on="on">
                        Nuevo Ticket
                    </v-btn>
                </template>
                <v-card>
                    <v-card-title>
                        <span class="text-h5">Ingrese los datos</span>
                    </v-card-title>
                    <v-card-text>
                        <v-form class="px-3" ref="form">
                            <v-container>
                                <v-row>
                                    <v-col cols="12">
                                        <v-select v-model="Sistema" :items="items" item-value="id" return-object
                                            :rules="sistemRules" label="Sistema" />
                                        <!-- <v-text-field label="Sistema" required v-model="Sistema" disable>
                                            <v-textarea>
                                            </v-textarea>
                                        </v-text-field> -->
                                    </v-col>
                                    <v-col cols="12">
                                        <v-text-field label="Nombre Y apellido" :rules="nameRules" required
                                            v-model="Requester">
                                            <v-textarea>
                                            </v-textarea>
                                        </v-text-field>
                                    </v-col>
                                    <v-col cols="12">
                                        <v-text-field label="Email" :rules="emailRules" required v-model="Email">
                                            >
                                            <v-textarea></v-textarea>
                                        </v-text-field>
                                    </v-col>
                                    <v-col cols="12">
                                        <v-text-field label="Asunto" :rules="subjectRules" required v-model="Subject">
                                            >
                                            <v-textarea></v-textarea>
                                        </v-text-field>
                                    </v-col>
                                    <v-col cols="12">
                                        <v-textarea label="Descripción" :rules="descriptionRules" required
                                            v-model="Description">
                                            <v-textarea></v-textarea>
                                        </v-textarea>
                                    </v-col>
                                </v-row>
                            </v-container>
                        </v-form>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="#26c6da" text @click="dialog = false">
                            Cerrar
                        </v-btn>
                        <v-btn color="#26c6da" text :disabled="isLoading" @click="aggregateItem(), dialogX = false">
                            Enviar
                        </v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-row>
        <v-spacer></v-spacer>

        <v-col>
            <template>
                <br>
                <v-card>
                    <v-card-title>
                        Filtrar Ticket
                        <v-spacer></v-spacer>
                        <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line
                            hide-details></v-text-field>
                    </v-card-title>
                </v-card>

                <v-data-table :headers="header" :items="rows" :search="search" class="elevation-1">
                    <template v-slot:item="row">
                        <tr>
                            <td>{{ row.item.Id }}</td>
                            <td>{{ row.item.Nombre }}</td>
                            <td>{{ row.item.Estado }}
                                <v-icon small class="mr-2" @click="editStatus(row.item)">
                                    mdi-pencil
                                </v-icon>
                            </td>
                            <td>{{ row.item.Sistema }}</td>
                            <td>{{ row.item.Asunto }}</td>
                            <td>
                                <v-icon small class="mr-2" @click="editItem(row.item)">
                                    mdi-plus
                                </v-icon>
                            </td>
                        </tr>
                    </template>
                </v-data-table>
            </template>
        </v-col>
        <v-dialog v-model="dialogUpdate" max-width="900px" persistent>
            <v-card>
                <v-card-title primary-title>
                    Agregar Comentario
                </v-card-title>
                <v-col cols="12">
                    <v-textarea v-model="edit_number">
                    </v-textarea>
                </v-col>
                <v-card-actions>
                    <v-btn color="#26c6da" text @click="dialogUpdate = false">
                        Cerrar
                    </v-btn>
                    <v-btn color="#26c6da" text :disabled="isLoading" @click="sendEdit()">
                        Enviar
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-dialog v-model="dialogStatus" max-width="900px" persistent>
            <v-card>
                <v-card-title primary-title>
                    Cambiar Estado
                </v-card-title>
                <v-col cols="12">
                    <v-select v-model="edit_status" :items="itemsStatus" item-value="id" return-object
                            label="Estado" />
                </v-col>
                <v-card-actions>
                    <v-btn color="#26c6da" text @click="dialogStatus = false">
                        Cerrar
                    </v-btn>
                    <v-btn color="#26c6da" text :disabled="isLoading" @click="sendEditStatus()">
                        Enviar
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>
<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';
import { IDataTable } from '@/model/main/IDataTable';
import { IHeaderTable } from '@/model/main/IHeaderTable';
import { internet } from '@/utils/Internet';
import Util from '@/utils/Util';
import { ILabels } from '@/model/label/ILabels';
import axios from "axios";


@Component({
    name: 'DataTable'
})
export default class DataTable {
    public rows: Array<IDataTable> = [];
    public header: Array<IHeaderTable<IDataTable>> = [];
    public isLoading = false;
    public data1: Array<ILabels> = [];
    public dialog = false;
    public search = "";
    public dialogX = false;
    public Id = "";
    public Estado = "";
    public sistemaa2 = "";
    public Sistema = "";
    public Requester = "";
    public nameRules = [
        (v: any) => !!v || 'Nombre y Apellido es obligatorio',
        (v: any) => (v && v.length <= 35) || 'Nombre y Apellido debe ser valido'
    ];
    public Email = "";
    public emailRules = [
        (v: any) => !!v || 'E-mail es obligatorio',
        (v: any) => /^(([^<>()[\]\\.,;:\s@']+(\.[^<>()\\[\]\\.,;:\s@']+)*)|('.+'))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(v) || 'E-mail debe ser valido'
    ];
    public Subject = "";
    public subjectRules = [
        (v: any) => !!v || 'Asunto es obligatorio',
        (v: any) => (v && v.length <= 250) || 'Asunto no debe superar los 250 caracteres'
    ];
    public Description = "";
    public descriptionRules = [
        (v: any) => !!v || 'Descripción es obligatorio',
        (v: any) => (v && v.length <= 250) || 'Descripción  no debe superar los 250 caracteres'
    ];
    public dialogUpdate = false;
    public dialogStatus = false;
    public dialogDelete = false;
    public edit_number = "";
    public edit_status = "";
    public select1: number;
    public items = ['Zendesk', 'Freshdesk'];
    public itemsStatus = ['open','pending', 'solved'];
    public sistemRules = [
        (v: any) => !!v || 'Sistema es obligatorio',
        (v: any) => (v && v.length <= 35) || 'Sistema debe ser valido'
    ]
    public current_item = { 'Id': '', 'Status':'' ,'Sistema': '', 'Requester': '', 'Email': '', 'Subject': '', 'Description': '', 'Comment1': '' };
    mounted(): void {
        this.getData();
    }


    private getData() {
        this.isLoading = true;
        let config = {
            method: 'get',
            url: 'http://127.0.0.1:9090/list',
            headers: { Authorization: 'Basic ' + btoa('usuario1' + ':' + 'usuario1'), "Content-Type": "application/json", "Accept": "*/*" },
        };
        axios(config)
            .then((response) => {
                let response1 = JSON.parse(response.data)
                this.data1 = response1;
                const dataTable: Array<IDataTable> = [];
                for (let item of this.data1) {
                    console.log(item);
                    const row: IDataTable = {};
                    row['Id'] = item.Id;
                    console.log(this.Id)
                    row['Nombre'] = item.Requester;
                    row['Estado'] = item.Status;
                    row['Sistema'] = item.Sistema;
                    row['Asunto'] = item.Subject;
                    row['Comentario'] = "";
                    //console.log(JSON.stringify(item.tunning))
                    dataTable.push(row);
                }
                const header: Array<IHeaderTable<
                    IDataTable
                >> = Object.keys(dataTable[0]).map(
                    (
                        key: string
                    ): IHeaderTable<IDataTable> => {
                        let text = key;
                        switch (key) {
                            case 'Requester':
                                text = "Nombre";
                                break;
                            case 'Sistema':
                                text = "Sistema";
                                break;
                            case 'Asunto':
                                text = "Asunto";
                                break;
                        }
                        return {
                            text,
                            value: key,
                        };
                    }
                ) as Array<IHeaderTable<IDataTable>>;
                console.log(dataTable)
                this.rows = dataTable;
                this.header = header;
            })
            .catch(console.log)
            .finally(() => {
                this.isLoading = false;
            });
    }

    public editItem(item: ILabels) {
        let comment = item.Comment1
        this.edit_number = comment;
        this.dialogUpdate = true;
        this.current_item = item;
        console.log(item)
    }
    public sendEdit() {
        let dt = JSON.stringify({
            'Sistema': this.current_item.Sistema,
            'Id': this.current_item.Id,
            'Comment1': this.edit_number
        })
        console.log(dt)
        let config = {
            method: 'post',
            url: 'http://127.0.0.1:9090/audit_ticket',
            data: dt,
            headers: {
                Authorization: 'Basic ' + btoa('usuario1' + ':' + 'usuario1'), "Content-Type": "application/json", "Accept": "*/*"
            }
        };
        axios(config)
            .then(response => {
                this.getData();
                this.dialogUpdate = false;
            })
    }

    public editStatus(item: ILabels) {
        let status = item.Status
        this.edit_status = status;
        this.dialogStatus = true;
        this.current_item = item;
        console.log(item)
    }

    public sendEditStatus() {

        let dt = JSON.stringify({
            'Sistema': this.current_item.Sistema,
            'Id': this.current_item.Id,
            'Status': this.edit_status
        })
        console.log(dt)
        let config = {
            method: 'post',
            url: 'http://127.0.0.1:9090/status',
            data: dt,
            headers: {
                Authorization: 'Basic ' + btoa('usuario1' + ':' + 'usuario1'), "Content-Type": "application/json", "Accept": "*/*"
            }
        };
        axios(config)
            .then(response => {
                this.getData();
                this.dialogStatus = false;
            })
    }

    public async aggregateItem() {
        if (this.$refs.form.validate()) {
            console.log(this.Sistema, this.Requester, this.Email, this.Description, this.Subject)
        }
        let Sistema1 = this.Sistema;
        let Requester1 = this.Requester;
        let Email1 = this.Email;
        let Subject1 = this.Subject;
        let Description1 = this.Description;
        let bodyContent = JSON.stringify({ "Sistema": Sistema1, "Requester": Requester1, "Email": Email1, "Subject": Subject1, "Description": Description1 })
        let config = {
            method: 'put',
            url: 'http://127.0.0.1:9090/audit_ticket',
            data: bodyContent,
            headers: { Authorization: 'Basic ' + btoa('usuario1' + ':' + 'usuario1'), "Content-Type": "application/json", "Accept": "*/*" }

        };
        let response = await axios.request(config)
            .then(response => {
                this.dialog = false;
                this.getData();
            })
    }
}
</script>