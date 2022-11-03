# Modern_Tetris_Clone
TechWithTim's PyGame Tetris game with bug fixes and modernized changes

Here are all the changes posted as patch notes:

### 1. Changed the randomization of the tetriminos to a more mordern randomizaton
   - The previous randomization of the game simply pulled one of the seven tetriminos randomly without any restrictions on what the next tetriminos can be. 
   This lead to some frustrating situations where a player could sometimes get multiple of the same tetriminos in a row.
   - The new randomization utilizes a "bag" system. This means that every seven tetriminos will be unique, and the most amount of repeating tetriminos a player can get is two
### 2. Extended the number of queued tetriminos from 1 to 4
   - Previewing only one tetrimino can lead to very short-sighted and reactive gameplay. Changing the number of previewed tetriminos from one to four should help players better plan out where they want to exactly put their tetriminos
   - Pairing this change with the new randomization not only modernizes the game, but also leads to a better gameplay flow
### 3. Added in a Shadow Tetrimino
   - The previous version didn't have a shadow tetrimino. Adding this in helps players see exactly where their tetrimino will fall
### 4. Added in a Fast Drop action
   - Pairing this with the added shadow tetrimino leads to the potentially for very fast gameplay
### 5. Added in a Holding Tetrimino function
   - With the addition of the holding piece function, players have a lot more flexibility with what tetrimino they play with. This addition in conjunction with both the new randomization and
   the extended queue make for a very modernized feel to the game.
   
#### Bug Fixes
- Fixed a bug that caused tetriminos to fly off the sides at the top of the grid if moved too quickly to the left or right at the beggining of play
- Fixed a bug that caused the game to crash if a tetrimino tried to move outside of the grid
- Fixed an issue with the tetriminos not being the correct color after the randomization changes
- Fixed a bug that caused empty rows to float when certain combinations of complete rows were deleted.
