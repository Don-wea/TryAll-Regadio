import { Component, OnInit } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common'; 

// Angular Material imports ...
import { MatTableModule } from '@angular/material/table';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatCardModule } from '@angular/material/card';

import { FormsModule } from '@angular/forms';
import { HistoricosService, Humedad, Temperatura, Flujo } from '../../services/historicos.service';
import { ChartType, ChartDataset, ChartOptions } from 'chart.js';
import { BaseChartDirective } from 'ng2-charts';
import { provideCharts, withDefaultRegisterables } from 'ng2-charts';

import { APIService } from '../../services/api.service';
import { SensorService } from '../../services/sensor.service';

// Interfaz para la zona con ID y Nombre
interface ZonaDisplay {
  id: string;
  nombre: string;
}

@Component({
  selector: 'app-history',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatTableModule,
    MatSelectModule,
    MatFormFieldModule,
    MatInputModule,
    MatCardModule,
    BaseChartDirective
  ],
  templateUrl: './history.component.html',
  styleUrl: './history.component.scss',
  providers: [
    provideCharts(withDefaultRegisterables()),
    DatePipe
  ]
})
export class HistoryComponent implements OnInit {

  zonas: ZonaDisplay[] = [];
  zonaSeleccionadaId: string = '';
  cantidadRegistros = 5;

  humedades: Humedad[] = [];
  temperaturas: Temperatura[] = [];
  flujos: Flujo[] = [];

  displayedColumnsHumedades: string[] = ['zona', 'sensor_id', 'valor', 'unidad', 'fecha_hora'];
  displayedColumnsTemperaturas: string[] = ['zona', 'sensor_id', 'valor', 'unidad', 'fecha_hora'];
  displayedColumnsFlujos: string[] = ['zona', 'regador_id', 'cantidad_agua_litros', 'energia_consumida_kwh', 'duracion_segundos', 'fecha_hora_inicio', 'fecha_hora_fin'];

  humedadChartData: ChartDataset[] = [];
  humedadChartLabels: string[] = [];
  humedadChartOptions: ChartOptions = { /* ... */ };
  humedadChartType: ChartType = 'line';

  temperaturaChartData: ChartDataset[] = [];
  temperaturaChartLabels: string[] = [];
  temperaturaChartOptions: ChartOptions = { /* ... */ };
  temperaturaChartType: ChartType = 'line';

  flujoChartData: ChartDataset[] = [];
  flujoChartLabels: string[] = [];
  flujoChartOptions: ChartOptions = { /* ... */ };
  flujoChartType: ChartType = 'bar';

  private zonaNombreMap: Map<string, string> = new Map();

  constructor(
    private historicosService: HistoricosService,
    private sensorService: SensorService,
    private apiService: APIService  // Inyectamos APIService
  ) {}

  ngOnInit() {
    this.cargarZonasDesdeAPI();
  }

  cargarZonasDesdeAPI() {
    this.apiService.getZonas().subscribe({
      next: (data: any[]) => {
        this.zonas = data.map(z => ({
          id: z.id || z._id || z.nombre, // ajusta según la estructura real
          nombre: z.nombre
        }));

        // Construimos el mapa id->nombre para uso posterior
        this.zonaNombreMap.clear();
        this.zonas.forEach(z => this.zonaNombreMap.set(z.id, z.nombre));

        // Luego que tenemos zonas, cargamos datos históricos
        this.cargarDatos();
      },
      error: (err) => {
        console.error('Error al cargar zonas:', err);
        // Igual intentar cargar datos históricos pero sin zonas
        this.cargarDatos();
      }
    });
  }

  cargarDatos() {
    this.historicosService.getUltimasHumedades(this.cantidadRegistros).subscribe(data => {
      this.humedades = this.zonaSeleccionadaId
        ? data.filter(d => d.zona_id === this.zonaSeleccionadaId)
        : data;

      this.humedades = this.humedades.map(h => ({ ...h, zona: this.zonaNombreMap.get(h.zona_id) || h.zona_id }));

      this.humedadChartData = [
        { data: this.humedades.map(h => h.valor), label: 'Humedad (%)' }
      ];
      this.humedadChartLabels = this.humedades.map(h => new Date(h.fecha_hora).toLocaleString());
    });

    this.historicosService.getUltimasTemperaturas(this.cantidadRegistros).subscribe(data => {
      this.temperaturas = this.zonaSeleccionadaId
        ? data.filter(d => d.zona_id === this.zonaSeleccionadaId)
        : data;

      this.temperaturas = this.temperaturas.map(t => ({ ...t, zona: this.zonaNombreMap.get(t.zona_id) || t.zona_id }));

      this.temperaturaChartData = [
        { data: this.temperaturas.map(t => t.valor), label: 'Temperatura' }
      ];
      this.temperaturaChartLabels = this.temperaturas.map(t => new Date(t.fecha_hora).toLocaleString());
    });

    this.historicosService.getUltimosFlujos(this.cantidadRegistros).subscribe(data => {
      this.flujos = this.zonaSeleccionadaId
        ? data.filter(d => d.zona_id === this.zonaSeleccionadaId)
        : data;

      this.flujos = this.flujos.map(f => ({ ...f, zona: this.zonaNombreMap.get(f.zona_id) || f.zona_id }));

      this.flujoChartData = [
        { data: this.flujos.map(f => f.cantidad_agua_litros), label: 'Agua (L)', yAxisID: 'y', type: 'bar' },
        { data: this.flujos.map(f => f.energia_consumida_kwh), label: 'Energía (kWh)', yAxisID: 'y1', type: 'line' }
      ];
      this.flujoChartLabels = this.flujos.map(f => new Date(f.fecha_hora_inicio).toLocaleString());
    });
  }

  actualizarDatos() {
    this.cargarDatos();
  }

  guardarLecturas() {
    this.sensorService.guardarLecturasActuales().subscribe({
      next: (response: any) => {
        console.log(response.mensaje);
        // this.mensajeRespuesta = 'Lecturas guardadas correctamente';
      },
      error: (error: any) => {
        console.error('Error al guardar lecturas:', error);
        // this.mensajeRespuesta = 'Error al guardar lecturas';
      }
    });
  }
}
