import {Component, input, output, signal} from '@angular/core';
import {FormsModule, NgForm} from '@angular/forms';
import {Movie} from '../../api/MovieModel';

@Component({
  selector: 'app-popup-modal',
  imports: [
    FormsModule
  ],
  templateUrl: './popup-modal.html',
  styleUrl: './popup-modal.scss',
})
export class PopupModal {
  readonly movie = input.required<Movie>()
  rating = signal<number>(0)

  readonly confirm = output<number>()
  readonly close = output<boolean>()

  onConfirm(form?: NgForm) {
    if( form?.invalid || this.rating() == -1) {
      form?.control.markAllAsTouched();
      return;
    }
    console.log("posted on Modal : ", this.rating())
    this.confirm.emit(this.rating() ?? -1);
  }

  onCancel() {
    this.close.emit(true);
  }
}
