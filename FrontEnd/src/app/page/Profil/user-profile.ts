import {Component, inject, OnInit, signal} from '@angular/core';
import {MovieService} from '../../api/service/movie-service';
import {DefaultUser, UserModel} from '../../api/UserModel';
import {ActivatedRoute} from '@angular/router';
import {Movie} from '../../api/MovieModel';
import {CondensedMovie} from '../../component/condensed-movie/condensed-movie';

@Component({
  selector: 'app-user-profile',
  imports: [
    CondensedMovie
  ],
  templateUrl: './user-profile.html',
  styleUrl: './user-profile.scss',
})
export class UserProfile implements OnInit {

  private movieService = inject(MovieService);
  private router = inject(ActivatedRoute)

  readonly user = signal<UserModel>(DefaultUser());
  readonly movies = signal<Movie[]>([]);

  ngOnInit() {
    this.router.queryParams.subscribe(params => {
      this.user.set({
        id: params["id"],
        username: params["username"],
        logged: params["logged"]
      })
    })
    this.loadData();
  }

  loadData() {
    this.movieService.get_movies().subscribe((movies : Movie[]) => {
      this.movies.set(movies);
      console.log(movies);
    })
  }

}
