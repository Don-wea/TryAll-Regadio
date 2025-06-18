import { Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { LayoutComponent } from './components/layout/layout.component';
import { LoginComponent } from './components/login/login.component';
import { MonitoreoComponent } from './components/monitoreo/monitoreo.component';
import { TESTComponent } from './components/test/test.component';
import { AuthGuard } from './guards/auth.guards';

export const routes: Routes = [
    { path: '', component: LayoutComponent, children: [
        { path: 'dashboard', component: DashboardComponent },
        { path: 'monitoreo', component: MonitoreoComponent },
        { path: 'TEST', component: TESTComponent},
    ], canActivate: [AuthGuard]},
    { path: "login", component: LoginComponent}

];
