import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { SensorService } from '../../services/sensor.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-control-de-flujo',
  imports: [ CommonModule, FormsModule, ReactiveFormsModule, RouterModule ],
  templateUrl: './control-de-flujo.component.html',
  styleUrl: './control-de-flujo.component.scss'
})
export class ControlDeFlujoComponent {
  cantidadFlujo = 0;
  flujo_actual = 0;
  flujo_objetivo = 0;  // Nuevo campo para el flujo objetivo
  mensajeRespuesta = '';

  ngOnInit() {
    // Obtener flujo actual cada segundo
    setInterval(() => {
      this.obtenerFlujo();
      this.obtenerFlujoObjetivo();  // Añadir llamada para obtener flujo objetivo
      console.log('Flujo actual:', this.flujo_actual);
      console.log('Flujo objetivo:', this.flujo_objetivo);
    }, 1000);
  }

  constructor(private http: HttpClient, private sensor: SensorService) {}

  obtenerFlujo() {
    this.sensor.getFlujoActual().subscribe({
      next: (data: any) => {
        this.flujo_actual = data.cantidad_flujo;
      },
      error: (error) => {
        console.error('Error al obtener flujo:', error);
      }
    });
  }

  obtenerFlujoObjetivo() {
    this.sensor.getFlujoObjetivo().subscribe({
      next: (data: any) => {
        this.flujo_objetivo = data.cantidad_flujo;
      },
      error: (error) => {
        console.error('Error al obtener flujo objetivo:', error);
      }
    });
  }

  enviarFlujo() {
    console.log('Enviando flujo:', this.cantidadFlujo);
    
    this.sensor.postFlujoObjetivo(this.cantidadFlujo).subscribe({
      next: (response: any) => {
        console.log('Respuesta completa del servidor:', response);
        this.mensajeRespuesta = `Flujo objetivo establecido: ${this.cantidadFlujo}`;
      },
      error: (error: any) => {
        console.error('Error completo:', error);
        
        // Imprimir detalles específicos del error
        if (error.error instanceof ErrorEvent) {
          // Error del lado del cliente
          console.error('Error del cliente:', error.error.message);
        } else {
          // Error del lado del servidor
          console.error('Código de error:', error.status);
          console.error('Cuerpo del error:', error.error);
        }
        
        this.mensajeRespuesta = 'Error al enviar el flujo objetivo';
      }
    });
  }

  // Método para limpiar el formulario
  limpiarFormulario() {
    this.cantidadFlujo = 0;
    this.mensajeRespuesta = '';
  }
}
