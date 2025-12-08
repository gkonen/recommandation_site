import {Component, input, ViewChild, ElementRef} from '@angular/core';
import {Movie} from '../../api/MovieModel';
import {CardMovie} from '../card-movie/card-movie';

@Component({
  selector: 'app-slider-movie',
  imports: [
    CardMovie
  ],
  templateUrl: './slider-movie.html',
  styleUrl: './slider-movie.scss',
})
export class SliderMovie {
  readonly movies_list = input.required<Movie[]>()

  @ViewChild('itemsWrapper', { static: false }) itemsWrapper!: ElementRef<HTMLDivElement>;

  private startX = 0;
  private currentTranslate = 0;
  private prevTranslate = 0;
  private isDragging = false;

  onDragStart(e: MouseEvent): void {
    this.startX = e.clientX;
    this.isDragging = true;
    this.setCursor('grabbing');
  }

  onDragMove(e: MouseEvent): void {
    if (!this.isDragging) return;

    const currentX = e.clientX;
    let newTranslate = this.prevTranslate + (currentX - this.startX);

    this.currentTranslate = this.clampTranslate(newTranslate);
    this.updateSliderPosition();
  }

  onDragEnd(): void {
    this.isDragging = false;
    this.prevTranslate = this.currentTranslate;
    this.setCursor('grab');
  }

  private clampTranslate(translate: number): number {
    // Limite moving to the right
    if (translate > 0) {
      return 0;
    }
    // Limite moving to the left
    const { containerWidth, contentWidth } = this.getSliderDimensions();
    const maxTranslate = containerWidth - contentWidth;

    return Math.max(translate, maxTranslate);
  }

  private getSliderDimensions() {
    const wrapper = this.itemsWrapper?.nativeElement;
    if (!wrapper) {
      return { containerWidth: 0, contentWidth: 0 };
    }

    const containerWidth = wrapper.parentElement?.clientWidth ?? 0;
    const contentWidth = wrapper.scrollWidth;

    return { containerWidth, contentWidth };
  }

  private setCursor(cursor: string): void {
    if (this.itemsWrapper) {
      this.itemsWrapper.nativeElement.style.cursor = cursor;
    }
  }

  private updateSliderPosition(): void {
    if (this.itemsWrapper) {
      this.itemsWrapper.nativeElement.style.transform =
        `translateX(${this.currentTranslate}px)`;
    }
  }
}
