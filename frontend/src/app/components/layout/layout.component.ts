//angular
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterOutlet } from '@angular/router';
import { routes } from '../../app.routes';

//angular material
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';

//my components
import { HeaderComponent } from '../header/header.component';
import { AuthService } from '../../auth/auth.service'; // Importa el servicio de autenticación
import { ChatIaComponent } from '../chat-ia/chat-ia.component';
// import { FooterComponent } from '../footer/footer.component';

@Component({
  selector: 'app-layout',
  imports: [
     MatSidenavModule,
     MatListModule,
     MatIconModule,
     MatButtonModule,
     CommonModule, 
     HeaderComponent, 
     ChatIaComponent,
    //  FooterComponent,
     RouterOutlet
  ],
  templateUrl: './layout.component.html',
  styleUrl: './layout.component.scss'
})
export class LayoutComponent {
  constructor (  //inyectamos el servicio y las rutas
    private router: Router,  // Paraa navegar entre páginas
    private route:ActivatedRoute,  //información de la ruta actual
    private authService: AuthService  // manejar el login/logout
    ) { }

  isActive(route: string): boolean {
    return this.router.url === route;
  }
  
  navigateToDashboard() {  // Función que nos lleva al dashboard
    this.router.navigate(['/dashboard']);
  } 
  navigateToChatbot() {  // Función que nos lleva al chatbot
    this.router.navigate(['/chat']);
  }
  navigateToMonitoreo(){  // Función que nos lleva a la home
    this.router.navigate(['/monitoreo']); 
  }

  navigateToTEST() {  // Función para ir a la página "About"
    this.router.navigate(['/TEST']);  
  }

  navigateToControlFLujo() {  // Función para ir a la página "Control Flujo"
    this.router.navigate(['/flujo']);  
  }
  
  navigateToHistory() {  // Función para ir a la página "Control Flujo"
    this.router.navigate(['/history']);  
  }
  // navigateToMyMap() {  // Función para ir a la página "Content"
  //   this.router.navigate(['/my-map']); 
  // }

  logout() {
    if (confirm('¿Estás seguro de que quieres cerrar sesión?')) {
      this.authService.logout();  // Llama al método de logout del servicio de autenticación
      this.router.navigate(['/login']);
    }
  }

}