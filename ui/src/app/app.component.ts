import { Component } from '@angular/core';
import { ChartOptions, ChartType, ChartDataSets } from 'chart.js';
import * as pluginDataLabels from 'chartjs-plugin-datalabels';
import { Label } from 'ng2-charts';
import { ApiService } from 'src/services/api.service';
import { timer } from 'rxjs';
import { take } from 'rxjs/operators';
import { formatDate } from '@angular/common';
import { environment } from 'src/environments/environment';
import { NgxSpinnerService } from 'ngx-spinner';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.sass']
})
export class AppComponent {
  public barChartOptions: ChartOptions = {
    responsive: true,
    // We use these empty structures as placeholders for dynamic theming.
    scales: { xAxes: [{}], yAxes: [{}] },
    plugins: {
      datalabels: {
        anchor: 'end',
        align: 'end',
      }
    }
  };
  public barChartType: ChartType = 'bar';
  public barChartLegend = false;
  public barChartPlugins = [pluginDataLabels];

  data:{title: string, barChartLabels: Label[], barChartData: ChartDataSets[]}[] = [];
  public barChartLabels: Label[] = ['2006', '2007', '2008', '2009', '2010', '2011', '2012'];
  public barChartData: ChartDataSets[] = [
    { data: [65, 59, 80, 81, 56, 55, 40], label: 'Series A' },
  ];

  constructor(private apiService: ApiService, private spinner: NgxSpinnerService) { }

  ngOnInit() {
    timer(1000, environment.frequency).subscribe(()=>this.refreshData())
  }

  refreshData(){
    const newData:{title: string, barChartLabels: Label[], barChartData: ChartDataSets[]}[] = [];
    this.spinner.show();
    this.apiService.getAllData().pipe(take(1)).subscribe(graphs=>{
      graphs.forEach(singleGraphData=>{
        const barChartData: ChartDataSets[] =[];
        const barChartLabels: Label[] = [];
        barChartData[0]  = {data:[], label: singleGraphData[0][2]}
        singleGraphData.forEach(singleData=>{
          barChartData[0]['data'].push(singleData[0]);
          barChartLabels.push(formatDate(singleData[1],environment.dateFormat,environment.locale,environment.timezone));
        })
        barChartData[0]['data'] = barChartData[0]['data'].reverse();
        
        newData.push({title:singleGraphData[0][3] ,barChartData: barChartData, barChartLabels: barChartLabels.reverse()})
      })

      this.data = newData;
      this.spinner.hide();
    });
    
  }

  // events
  public chartClicked({ event, active }: { event: MouseEvent, active: {}[] }): void {
    console.log(event, active);
  }

  public chartHovered({ event, active }: { event: MouseEvent, active: {}[] }): void {
    console.log(event, active);
  }

}
