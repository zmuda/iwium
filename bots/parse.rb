require 'json'
content = JSON.parse(File.read("GAME_STATES.out"))

(0..2).each do |i|
  puts i
  puts "result " + content.map { |c| c[-3..-1][i].to_i }.inject(:+).to_s
  puts "did not win with best card " + content.map { |c| [c[0..2], c[-3..-1]] }.select { |e| e[0].uniq.size == 3 && e[1].rindex(e[1].max) != i &&  e[0].rindex(e[0].max) == i }.size.to_s
  puts "won without best card " + content.map { |c| [c[0..2], c[-3..-1]] }.select { |e| e[0].uniq.size == 3 && e[1].rindex(e[1].max) != e[0].rindex(e[0].max) && e[1].rindex(e[1].max) == i  }.size.to_s
  puts "---"
end
