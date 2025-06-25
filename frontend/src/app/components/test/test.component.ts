import { Component } from '@angular/core';
import { SensorService } from '../../services/sensor.service';
import { HistoricosService, Humedad, Temperatura, Flujo } from '../../services/historicos.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-test',
  imports: [CommonModule],
  templateUrl: './test.component.html',
  styleUrl: './test.component.scss'
})
export class TESTComponent {

  datoTemperaturaReal = 0;
  datoHumedadReal = 0;
  datoFlujoReal = 0;

  listaHumedad: Humedad[] = [];
  listaTemperatura: Temperatura[] = [];
  listaFlujo: Flujo[] = [];

  constructor(private sensorService: SensorService, private historicosService: HistoricosService) { }

  ngOnInit(): void {
    this.llenarHumedad();
    this.llenarTemperatura();
    this.llenarFlujo();

    // Llama a la función para actualizar datos cada segundo
    setInterval(() => {
      this.HumedadyTiempoReal();
      this.flujoTiempoReal();

      if (this.datoHumedadReal && this.listaHumedad.length > 0) {
        this.listaHumedad.push({
          ...this.listaHumedad[this.listaHumedad.length - 1],
          valor: Number(this.datoHumedadReal),
          fecha_hora: new Date().toISOString()
        });
        this.listaHumedad.shift();
      }
      if (this.datoTemperaturaReal && this.listaTemperatura.length > 0) {
        this.listaTemperatura.push({
          ...this.listaTemperatura[this.listaTemperatura.length - 1],
          valor: Number(this.datoTemperaturaReal),
          fecha_hora: new Date().toISOString()
        });
        this.listaTemperatura.shift();
      }

    }, 1000); // cada segundo
  }

  llenarHumedad() {
    // Simulación de llamada al endpoint
    this.historicosService.getUltimasHumedades(10).subscribe((data: any[]) => {
      this.listaHumedad = data;
    });
  }

  llenarTemperatura() {
    this.historicosService.getUltimasTemperaturas(10).subscribe((data: any[]) => {
      this.listaTemperatura = data;
    });
  }

  llenarFlujo() {
    this.historicosService.getUltimosFlujos(10).subscribe((data: any[]) => {
      this.listaFlujo = data;
    });
  }

  HumedadyTiempoReal(){
    this.sensorService.getHumedadTemperaturaActual().subscribe((data: any) => {
      this.datoHumedadReal = data.humedad;
      this.datoTemperaturaReal = data.temperatura;
    });
  }

  humedadTiempoReal() {
    this.sensorService.getHumedadActual().subscribe((data: any) => {
      this.datoHumedadReal = data.humedad;
    });
  }

  temperaturatTiempoReal() {
    this.sensorService.getTemperaturaActual().subscribe((data: any) => {
      this.datoTemperaturaReal = data.temperatura;
    });
  }

  flujoTiempoReal() {
    this.sensorService.getFlujoActual().subscribe((data: any) => {
      this.datoFlujoReal = data.flujo_actual;
    });
  }
}
