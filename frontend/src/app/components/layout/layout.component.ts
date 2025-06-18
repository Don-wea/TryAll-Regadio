//angular
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterOutlet } from '@angular/router';
import { routes } from '../../app.routes';

//angular material
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';

//my components
import { HeaderComponent } from '../header/header.component';
// import { FooterComponent } from '../footer/footer.component';

@Component({
  selector: 'app-layout',
  imports: [
     MatSidenavModule,
     MatListModule, 
     CommonModule, 
     HeaderComponent, 
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
    // private authService: AuthService  // manejar el login/logout
    ) { }
  
  navigateToDashboard() {  // Función que nos lleva al dashboard
    this.router.navigate(['/dashboard']);
  } 
   
  navigateToMonitoreo(){  // Función que nos lleva a la home
    this.router.navigate(['/monitoreo']); 
  }

  navigateToTEST() {  // Función para ir a la página "About"
    this.router.navigate(['/TEST']);  
  }

  // navigateToMyMap() {  // Función para ir a la página "Content"
  //   this.router.navigate(['/my-map']); 
  // }

}