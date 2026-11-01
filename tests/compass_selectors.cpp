#include "sd.h"
#include <cassert>
#include <cstring>

extern selector_kind fix_short_other_selector(selector_kind);

static int selected(const setup &s, int place, selector_kind selector)
{
   current_options.who.who[0] = selector;
   try { return selectp(&s, place); }
   catch (error_flag_type) { return -1; }
}

int main()
{
   // A rectangular formation rotated through all four caller-relative axes.
   for (int rotation = 0; rotation < 4; rotation++) {
      setup s;
      s.kind = s2x4;
      s.rotation = rotation;
      s.eighth_rotation = 0;
      s.clear_people();
      for (int i = 0; i < 8; i++) s.people[i].id1 = i & 1 ? d_east : d_north;
      s.put_in_absolute_proximity_and_facing_bits();
      for (int i = 0; i < 8; i++) {
         const coordrec *coords = setup_attrs[s.kind].nice_setup_coords;
         int horizontal = rotation & 1 ? -coords->yca[i] : coords->xca[i];
         int vertical = rotation & 1 ? coords->xca[i] : -coords->yca[i];
         if (rotation & 2) { horizontal = -horizontal; vertical = -vertical; }
         assert(selected(s, i, selector_north_facers) == selected(s, i, selector_facingfront));
         assert(selected(s, i, selector_south_facers) == selected(s, i, selector_facingback));
         assert(selected(s, i, selector_east_facers) == selected(s, i, selector_facingleft));
         assert(selected(s, i, selector_west_facers) == selected(s, i, selector_facingright));
         assert(selected(s, i, selector_north) == (vertical > 0));
         assert(selected(s, i, selector_south) == (vertical < 0));
         assert(selected(s, i, selector_north) == selected(s, i, selector_nearfour));
         assert(selected(s, i, selector_south) == selected(s, i, selector_farfour));
         assert(selected(s, i, selector_east) == (horizontal < 0));
         assert(selected(s, i, selector_west) == (horizontal > 0));
         assert(selected(s, i, selector_northerners) == selected(s, i, selector_north));
         assert(selected(s, i, selector_southerners) == selected(s, i, selector_south));
         assert(selected(s, i, selector_easterners) == selected(s, i, selector_east));
         assert(selected(s, i, selector_westerners) == selected(s, i, selector_west));
         assert(selected(s, i, selector_east_4) == selected(s, i, selector_east));
         assert(selected(s, i, selector_west_4) == selected(s, i, selector_west));
         assert(selected(s, i, selector_north_box) == selected(s, i, selector_nearbox));
         assert(selected(s, i, selector_south_box) == selected(s, i, selector_farbox));
         assert(selected(s, i, selector_east_box) == selected(s, i, selector_boxleft));
         assert(selected(s, i, selector_west_box) == selected(s, i, selector_boxright));
      }
      s.clear_absolute_proximity_and_facing_bits();
      for (int i = 0; i < 8; i++)
         assert(!(s.people[i].id3 & (ID3_EASTFOUR | ID3_WESTFOUR)));
   }

   // A vertical line has no unambiguous caller-left/caller-right half.
   setup line;
   line.kind = s1x8;
   line.rotation = 1;
   line.eighth_rotation = 0;
   line.clear_people();
   for (int i = 0; i < 8; i++) line.people[i].id1 = d_north;
   line.put_in_absolute_proximity_and_facing_bits();
   for (int i = 0; i < 8; i++) {
      assert(!(line.people[i].id3 & (ID3_EASTFOUR | ID3_WESTFOUR)));
      assert(selected(line, i, selector_east) == -1);
      assert(selected(line, i, selector_easterners) == -1);
      assert(selected(line, i, selector_westerners) == -1);
   }

   assert(strcmp(selector_list[selector_north].name, "north") == 0);
   assert(strcmp(selector_list[selector_west_box].name, "west box") == 0);
   assert(selector_list[selector_north_2].opposite == selector_farsix);
   assert(strcmp(selector_list[selector_northerners].name, "northerners") == 0);
   assert(selector_list[selector_northerners].opposite == selector_southerners);
   assert(strcmp(selector_list[selector_southerners].name, "southerners") == 0);
   assert(selector_list[selector_southerners].opposite == selector_northerners);
   assert(strcmp(selector_list[selector_easterners].name, "easterners") == 0);
   assert(selector_list[selector_easterners].opposite == selector_westerners);
   assert(strcmp(selector_list[selector_westerners].name, "westerners") == 0);
   assert(selector_list[selector_westerners].opposite == selector_easterners);
   two_couple_calling = true;
   assert(fix_short_other_selector(selector_north_2) == selector_fartwo);
   assert(fix_short_other_selector(selector_south_3) == selector_nearest1);
   two_couple_calling = false;
}
