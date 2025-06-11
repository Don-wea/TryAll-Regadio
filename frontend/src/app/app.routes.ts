import { Routes } from '@angular/router';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { LayoutComponent } from './components/layout/layout.component';
import { LoginComponent } from './components/login/login.component';
import { TESTComponent } from './components/test/test.component';

export const routes: Routes = [
    { path: '', component: LayoutComponent, children: [
        { path: 'dashboard', component: DashboardComponent },
        { path: 'TEST', component: TESTComponent},
    ]},
    { path: "login", component: LoginComponent}

];
