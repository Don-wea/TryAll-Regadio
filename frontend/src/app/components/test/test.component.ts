import { Component } from '@angular/core';
import { SensorService } from '../../services/sensor.service';

@Component({
  selector: 'app-test',
  imports: [],
  templateUrl: './test.component.html',
  styleUrl: './test.component.scss'
})
export class TESTComponent {

  sensor: any = [];
  datoTiempoReal = ""

  constructor(private sensorService: SensorService) { }

  ngOnInit(): void {
    setInterval(() => {
      this.sensorService.getHumedadActual().subscribe((data: any) => {
        this.datoTiempoReal = data.humedad;
      });
    }, 1000); // cada segundo
  }
  

  humedadTiempoReal() {
    this.sensorService.getHumedadActual().subscribe((data: any) => {
      this.datoTiempoReal = data.humedad; // <-- aquí se actualiza con la respuesta real
    });
  }
}
