#include <ncurses.h>
#include <string.h>
#include <signal.h>

// SIGWINCH is called when the window is resized.
void handle_winch(int sig){
  signal(SIGWINCH, SIG_IGN);

  // Reinitialize the window to update data structures.
  endwin();
  initscr();
  refresh();
  clear();

  char tmp[128];
  sprintf(tmp, "%dx%d", COLS, LINES);

  // Approximate the center
  int x = COLS / 2 - strlen(tmp) / 2;
  int y = LINES / 2 - 1;

  mvaddstr(y, x, tmp);
  refresh();

  signal(SIGWINCH, handle_winch);
}

int main(int argc, char *argv[]){
/*  if(!has_colors()){
  printw("no color");
  getch();
  return 1;
  }*/
  start_color();
  init_pair(1,COLOR_CYAN,COLOR_BLACK); 
  initscr();
  cbreak();
  noecho();
  signal(SIGWINCH, handle_winch);
  int height, width, start_x, start_y;
  height = LINES;
  width = COLS;
  start_x = start_y = 0;

  WINDOW * win  = newwin(height, width, start_x,start_y);
  refresh();
  //box(win,0,0);
  int left, right, top, bottom, tlc, trc, blc, brc;
  left = right = 0;
  top = bottom = 0;
  char ast = '+';
  tlc = trc = blc = brc = (int)ast;
  wborder(win,left,right,top,bottom,tlc,trc,blc,brc);
  mvwprintw(win,1,1, "This is a box");
  mvwprintw(win,2,1,"___________________________");
  wrefresh(win);


  
  
  while(getch() != 27){
    /* Nada */
  }

  endwin();

  return(0);
}
