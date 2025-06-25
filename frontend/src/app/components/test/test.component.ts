import { Component } from '@angular/core';
import { SensorService } from '../../services/sensor.service';

@Component({
  selector: 'app-test',
  imports: [],
  templateUrl: './test.component.html',
  styleUrl: './test.component.scss'
})
export class TESTComponent {

  datoTemperaturaReal = 0;
  datoHumedadReal = 0;
  datoFlujoReal = 0;

  constructor(private sensorService: SensorService) { }

  ngOnInit(): void {
    // Llama a la función para actualizar datos cada segundo
    setInterval(() => {
      this.HumedadyTiempoReal();
      this.flujoTiempoReal();
    }, 1000); // cada segundo
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
