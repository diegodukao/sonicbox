# Run this script in a Sonic Pi buffer for Sonicbox to work


use_real_time

live_loop :samples do
  name = sync "/osc/sample"
  sample name
end

live_loop :synths do
  synth_name, tonic, name, note_num = sync "/osc/synth"
  use_synth synth_name.to_sym
  play scale(tonic, name, num_octaves: 7)[note_num]
end

live_loop :drum_machine do
  set_list = sync "/osc/drum-machine"
  set_list.each do |set|
    sample :loop_amen, onset: set
  end
end

live_loop :chord_prog do
  synth_name, tonic, type, key_degree = sync "/osc/chord-prog"
  use_synth synth_name.to_sym
  play (chord_degree key_degree.to_sym, tonic, type, 3)
end