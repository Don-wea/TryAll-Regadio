import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SaludoService } from '../../services/saludo.service'; // Nueva importación

@Component({
  selector: 'app-dashboard',
  imports: [CommonModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent {

  constructor(private saludoService: SaludoService) {} // Inyección del servicio

  solicitudTest() {
    this.saludoService.getSaludo().subscribe({
        next: (response) => {
            // Manejar respuesta exitosa con el mensaje de Django
            alert(response.mensaje);
        },
        error: (error) => {
            // Manejar errores de conexión o del servidor
            console.error('Error:', error);
            alert('Error al conectar con el backend');
        }
    });
}
}