import {inject, Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {UserModel} from '../UserModel';
import {map} from 'rxjs';
import {ResponseData} from '../UserDataModel';

@Injectable({
  providedIn: 'root',
})
export class UserService {
  private url = 'http://localhost:5000/';
  private http = inject(HttpClient);

  connect(username:string, password:string)  {
    return this.http.post<UserModel>(this.url + 'users/login', {
      username: username, password: password
    }, {
      headers: {
        'Content-Type': 'application/json'
      }
    }).pipe(
      map(response => ({
        logged: response.logged,
        username: username,
        id: response.id
      }))
    )
  }

  get_user_data(user: UserModel) {
    return this.http.get<ResponseData>(this.url + 'users/' + user.id).pipe(
      map(response => ({
        ratings: response.ratings,
        tags: response.tags,
        })
      )
    );
  }

}
