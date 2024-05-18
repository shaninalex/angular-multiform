import { Component } from '@angular/core';
import { ApiPositionService } from '../services/position.service';
import { Position } from '../types';

@Component({
    selector: 'app-assignemnt-page',
    templateUrl: './assignemnt-page.component.html',
})
export class AssignemntPageComponent {
    positions: Position[] = [];
    visible: boolean = false;
    positionId: number;

    constructor(private positionsApi: ApiPositionService) {
        this.positionsApi.list().subscribe({
            next: results => { this.positions = results.data }
        })
    }

	open(positionId: number) {
        this.positionId = positionId;
        this.visible = true;
	}
}
