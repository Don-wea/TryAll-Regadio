import { Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { LayoutComponent } from './components/layout/layout.component';
import { LoginComponent } from './components/login/login.component';
import { MonitoreoComponent } from './components/monitoreo/monitoreo.component';
import { TESTComponent } from './components/test/test.component';

import { ControlDeFlujoComponent } from './components/control-de-flujo/control-de-flujo.component';

import { AuthGuard } from './guards/auth.guards';

export const routes: Routes = [
    { 
        path: '', 
        component: LayoutComponent, 
        children: [
            { path: '', redirectTo: 'monitoreo', pathMatch: 'full' },
            // { path: 'dashboard', component: DashboardComponent },
            { path: 'monitoreo', component: MonitoreoComponent },
            { path: 'TEST', component: TESTComponent},
            { path: 'flujo', component: ControlDeFlujoComponent}
        ],
        canActivate: [AuthGuard] // This is where the AuthGuard should be placed
    },
    { path: "login", component: LoginComponent}
];