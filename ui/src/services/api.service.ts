import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { DataModel } from 'src/models/data.model';
import { environment } from 'src/environments/environment';
import { catchError, retry, concatMap, mergeAll, concatAll, timeout } from 'rxjs/operators';
import { throwError, Observable, merge, of, zip, forkJoin } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }

  getAllData(){
    const list: Observable<DataModel[]>[] = [];

    environment.codes.forEach(code => {
      list.push(this.getDataByCode(code));
    });

    return forkJoin(list);
  }

  getDataByCode(code: string):Observable<DataModel[]> {
    return this.http.get<DataModel[]>(`${environment.apiHost}/api/people/${code}`)
      .pipe(
        retry(3), // retry a failed request up to 3 times
        timeout(5000),
        catchError(this.handleError) // then handle the error
      );
  }

  private handleError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {
      // A client-side or network error occurred. Handle it accordingly.
      console.error('An error occurred:', error.error.message);
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong,
      console.error(
        `Backend returned code ${error.status}, ` +
        `body was: ${error.error}`);
    }
    // return an observable with a user-facing error message
    return throwError(
      'Something bad happened; please try again later.');
  };
}
