import { Component, OnInit } from '@angular/core';
import { APIService } from '../../services/api.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-monitoreo',
  imports: [CommonModule],
  templateUrl: './monitoreo.component.html',
  styleUrl: './monitoreo.component.scss'
})

export class MonitoreoComponent implements OnInit {
  zonas: any[] = [];
  nodos: any[] = [];
  sensores: any[] = [];
  lecturasZona: any[] = [];
  lecturasSensor: any[] = [];
  alertas: any[] = [];

  zonaActual: any = null;
  indiceZonaActual: number = 0;

  constructor(private apiService: APIService) {}

  ngOnInit() {
    this.cargarZonas();
  }

  cargarZonas() {
    this.apiService.getZonas().subscribe(data => {
      this.zonas = data;
      if (this.zonas.length > 0) {
        this.indiceZonaActual = 0;
        this.zonaActual = this.zonas[0];
        this.cargarDatosZona(this.zonaActual.id);
      }
    });
  }

  cargarDatosZona(zonaId: string) {
    // Cargar nodos de la zona
    this.apiService.getNodosPorZona(zonaId).subscribe(nodos => {
      this.nodos = nodos;
      // Cargar sensores de todos los nodos
      this.sensores = [];
      if (this.nodos.length > 0) {
        this.nodos.forEach(nodo => {
          this.cargarSensoresNodo(nodo.id);
        });
      }
    });

    // Cargar lecturas de la zona
    this.apiService.getLecturasPorZona(zonaId).subscribe(lecturas => {
      this.lecturasZona = lecturas;
      this.procesarAlertas(lecturas);
    });
  }

  cargarSensoresNodo(nodoId: string) {
    this.apiService.getSensoresPorNodo(nodoId).subscribe(sensores => {
      this.sensores = [...this.sensores, ...sensores];
    });
  }

  cambiarZona(direccion: 'anterior' | 'siguiente') {
    if (!this.zonas || this.zonas.length === 0) return;
    
    if (direccion === 'anterior') {
      this.indiceZonaActual = this.indiceZonaActual === 0 ? this.zonas.length - 1 : this.indiceZonaActual - 1;
    } else {
      this.indiceZonaActual = this.indiceZonaActual === this.zonas.length - 1 ? 0 : this.indiceZonaActual + 1;
    }
    
    this.zonaActual = this.zonas[this.indiceZonaActual];
    this.cargarDatosZona(this.zonaActual.id);
  }

  procesarAlertas(lecturas: any[]) {
    // Aquí procesaríamos las lecturas para generar alertas basadas en umbrales
    // Por ahora, usamos datos de ejemplo
    this.alertas = [];
    
    // Ejemplo: si hay lecturas con valores extremos, generamos alertas
    lecturas.forEach(lectura => {
      if (lectura.tipo === 'humedad_suelo' && lectura.valor < 30) {
        this.alertas.push({
          tipo: 'danger',
          titulo: 'Humedad Baja',
          zona: this.zonaActual.nombre,
          fecha: new Date(lectura.fecha_hora).toLocaleString(),
        });
      }
      if (lectura.tipo === 'temperatura' && lectura.valor > 30) {
        this.alertas.push({
          tipo: 'warning',
          titulo: 'Temperatura Alta',
          zona: this.zonaActual.nombre,
          fecha: new Date(lectura.fecha_hora).toLocaleString(),
        });
      }
    });
  }
}