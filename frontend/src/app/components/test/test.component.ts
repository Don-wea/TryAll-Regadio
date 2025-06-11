import { Component } from '@angular/core';
import { SensorService } from '../../services/sensor.service';

@Component({
  selector: 'app-test',
  imports: [],
  templateUrl: './test.component.html',
  styleUrl: './test.component.scss'
})
export class TESTComponent {

  datoTiempoReal = "";
  porcentajeTiempoReal = "";

  constructor(private sensorService: SensorService) { }

  ngOnInit(): void {
    setInterval(() => {
      this.sensorService.getHumedadActual().subscribe((data: any) => {
        this.datoTiempoReal = data.humedad;
        const raw = parseInt(this.datoTiempoReal);
        this.porcentajeTiempoReal = ((raw / 4095) * 100).toFixed(2) + '%';
      });
    }, 1000); // cada segundo
  }
  

  humedadTiempoReal() {
    this.sensorService.getHumedadActual().subscribe((data: any) => {
      this.datoTiempoReal = data.humedad;
      const raw = parseInt(this.datoTiempoReal);
      this.porcentajeTiempoReal = ((raw / 4095) * 100).toFixed(2) + '%';
    });
  }
}
