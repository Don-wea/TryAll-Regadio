import { Component } from '@angular/core';
import { APIService } from '../../services/api.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-monitoreo',
  imports: [CommonModule],
  templateUrl: './monitoreo.component.html',
  styleUrl: './monitoreo.component.scss'
})

export class MonitoreoComponent {

  zonas: any[] = [];
  nodos: any[] = [];
  sensores: any[] = [];
  lecturasZona: any[] = [];
  lecturasSensor: any[] = [];

  zonaSeleccionada: string = '';
  nodoSeleccionado: string = '';
  sensorSeleccionado: string = '';

  constructor(private apiService: APIService) {}

  cargarZonas() {
    this.apiService.getZonas().subscribe(data =>
      this.zonas = data
    );
  }

  verNodos(zonaId: string) {
    this.apiService.getNodosPorZona(zonaId).subscribe(data =>
      this.nodos = data
    );
    this.nodos = [];
    this.sensores = [];
    this.lecturasSensor = [];
  }

  verSensores(nodoId: string) {
    this.apiService.getSensoresPorNodo(nodoId).subscribe(data =>
      this.sensores = data
    );
    this.sensores = [];
    this.lecturasSensor = [];
  }

  verLecturasZona(zonaId: string) {
    this.apiService.getLecturasPorZona(zonaId).subscribe(data =>
      this.lecturasZona = data
    );
  }

  verLecturasSensor(sensorId: string) {
    this.apiService.getLecturasPorSensor(sensorId).subscribe(data =>
      this.lecturasSensor = data
    );
  }

}
