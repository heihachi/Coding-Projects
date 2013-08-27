#!/home/jamez/ruby/bin/ruby
require 'socket'
#require 'serverinfo.rb'
require 'rubygems'
require 'mysql'
require 'whenever'

#######################################################################################################
 
# File Needs to be named anything with a .rb after it.
if File.exists?("serverinfo.rb")
    #print "Do you want to load your IRC data from the serverinfo.rb file? >> "
    #file_open = gets.chomp
    file_open = 'yes'

else
   print "What server to connect to >> "                                                                
   $server = gets.chomp                                                                                                         
   print "Port to connect to >> "                                                                                               
   $port = gets.chomp                                                                                                           
   print "Channel to join >> "                                                                          
   $channel = gets.chomp                                                                                
   print "Desired Nick >> "                                                                                                     
   $nick = gets.chomp                                                                                                           
   @channel = '#{$channel}'                                                                                                     
end 

if file_open == 'no'
    print "What server to connect to >> "                                                                
    $server = gets.chomp 
    print "Port to connect to >> "                                                                                               
    $port = gets.chomp                                                                                                           
    print "Channel to join >> "                                                                          
    $channel = gets.chomp                                                                                
    print "Desired Nick >> "                                                                                                     
    $nick = gets.chomp                                                                                                           
    @channel = '#{$channel}'
end

if file_open == "yes"                                                                                                           
   #file = File.new("serverinfo.rb", "r")
   eval File.open('serverinfo.rb').read
   $user=@user
   $pass=@pass
end                                                                                                                          
#######################################################################################################
#                                                                                                                               #
#######################################################################################################
class SimpleIrcBot

    def initialize(server, channel)
        server = '#{$server}'
        @channel = '#{$channel}'
        print "Connecting to #{$server}:#{$port}\n"
        print "Channel is #{$channel}:#{$chanpass}\n"
        print "Nick is #{$nick}\n"
        port = #{$port}
        #print $user
        #print $pass
        @socket = TCPSocket.open($server, $port)
        say "NICK #{$nick}"
        sleep(2)
        say "USER test 0 * Test"
#        sleep(2)
#        say "JOIN #{$channel} #{$chanpass}"
	sleep(2)
	say "PART #{$part}"
	sleep(5)
	say "JOIN #{$channel} #{$chanpass}"
	end
    def say(msg)
        puts msg
        @socket.puts msg
    end
    def say_to_chan(msg)
        say "PRIVMSG #{$channel} :#{msg}"
    end
    def sayArray(msg)
        puts msg
        @socket.puts msg
    end
    def array_to_chan(msg)
        msg = msg.map(&:inspect).join(", ").tr('"', '')
        msg = msg.tr(',', '|')
        puts msg
        sayArray "PRIVMSG #{$channel} :#{msg}"
    end  
    def sendraw(s)
        raise "Message too long" if s.length > 510
        s << "rn" unless s =~ /rn$/
        @sock.write s
    end
    def send(t, m)
        sendraw "PRIVMSG #{t} :#{m}"
    end  
    def run
        until @socket.eof? do
            my_file = File.new("log.log", "w")
            msg = @socket.gets
            puts msg
            chan_1 = msg.match(/PRIVMSG #{$channel} :(.*)S/)
            open('log.log', 'a') { |f| f.puts "#{chan_1}" }
        	#logging = my_file.puts "#{msg}"
            log_size = File.size("log.log")
            if log_size >= 102400000
                if File.exists?("logchecker.log")
                    x = 1
                else
                    system 'python email_logger.py'
                    my_file2 = File.new("logchecker.log", "a")
                    my_file2.close
                    my_file.close
                    File.rename( "log.log", "log1.log")
                end
			end
			if log_size <= 102400000
				if File.exists?("logchecker.log")
					File.delete("logchecker.log")
				else
					y = 1
				end
			end	
            if msg.match(/^PING :(.*)$/)
                    say "PONG #{$~[1]}"
                    next
            end

            if msg.match(/PRIVMSG #{$channel} :(.*)$/) || msg.match(/PRIVMSG #{$nick} :(.*)$/)
                content = $~[1]
                words = msg.split(" ")
                $sender = msg.scan(/\A:(.*?)\!/)
                $sender = $sender.map(&:inspect).join(", ").tr('["]', '')
        
                #put matchers here
                if content.match('\A#online')
                    online = Array.new
                    con = Mysql.new('localhost', $user, $pass, 'characters')
                    result = con.query("SELECT * from gm_tickets where `name` in (select `name` from `characters`.`characters` where `online` = 1) AND `closedBy` = 0;")
                    if result.num_rows > 0
                        result.each_hash do |j|
                        id=j['ticketId']
                        player=j['name'].gsub(/[\n\r]+/, " ")
                        message = "#{player}: #{id}"
                        online.push(message)
                        end
                        con.close
                        array_to_chan(online)
                    else
                        say_to_chan("#{$sender}: There are currently no online tickets.")
                    end
                end
                if content.match('\A#staff')
                    staff = Array.new
                    con = Mysql.new('localhost', $user, $pass, 'characters')
                    result = con.query("SELECT `name` from `characters`.`characters` where `account` in (select `id` from `realmd`.`account_access` where `RealmID` in (-1)) and `online` = 1;")
                    if result.num_rows > 0
                        result.each_hash do |j|
                            result2 = con.query("SELECT `gmlevel` FROM `realmd`.`account_access` WHERE `id` in (SELECT `account` FROM `characters`.`characters` WHERE `name` = '#{j['name']}') AND `RealmID` = -1;")
                            result2.each_hash do |k|
                                if k['gmlevel'] == '1'
                                    staff.push("[MOD]#{j['name']} ")
                                elsif k['gmlevel'] == '2'
                                    staff.push("[GM]#{j['name']} ")
                                elsif k['gmlevel'] == '3'
                                    staff.push("[SGM]#{j['name']} ")
                                elsif k['gmlevel'] == '4'
                                    staff.push("[ADMIN]#{j['name']} ")
                                elsif k['gmlevel'] == '5'
                                    staff.push("[OWNER]#{j['name']} ")
                                    #staff.push("#{j['name']} ")
                                end
                            end
                        end
                        con.close
                        array_to_chan("Online Staff: #{staff}")
                    else
                        say_to_chan("#{$sender}: There are no staff members online.")
                    end
                end
				if content.match('\A#player')
					player = Array.new
					s = content
					name = s.split(' ')[1]
					name = name.capitalize
					con = Mysql.new('localhost', $user, $pass, 'characters')
					result = con.query("SELECT * FROM `characters` WHERE `name` = '#{name}';")
					if result.num_rows > 0
						result.each_hash do |h|
							id=h['account']
							result2 = con.query("SELECT name FROM characters WHERE account = '#{id}' AND online = 1;")
							if result2.num_rows == 1
								result2.each_hash do |a|
									say_to_chan("#{$sender}: They are on #{a['name']}")
								end
							else
								say_to_chan("#{$sender}: They are not online.")
							end
						end
					end
				end
                if content.match('\A#tickets')
                    tickets = Array.new
                    con = Mysql.new('localhost', $user, $pass, 'characters')
                    result = con.query("SELECT * from gm_tickets where `closedBy` = 0;")
                    if result.num_rows == 0
                        say_to_chan("#{$sender}: There are currently no tickets.")
                    else
                        result.each_hash do |j|
                        id=j['ticketId']
                        player=j['name'].gsub(/[\n\r]+/, " ")
                        #message=h['message'].gsub(/[\n\r]+/, " ")
                        #say_to_chan("Ticket:'#{id}'")
                        #say_to_chan("Ticket: #{id} | Player: #{player}") end
                        message = "#{player}: #{id} "
                        #say "PRIVMSG #{$sender} #{message}"
                        tickets.push(message)
                        end
                        con.close
                        array_to_chan(tickets)
                    end
                end
                if content.match('\A#viewticket')
                    s = content
                    id = s.split(' ')[1]
                    id = id.to_i
                    check = id.kind_of?(Numeric)
                    if check == true
                        if id != 0
                            tickets = Array.new
                            con = Mysql.new('localhost', $user, $pass, 'characters')
                            result = con.query("SELECT * FROM `gm_tickets` WHERE `ticketId` = '#{id}' AND `closedBy` = 0;")
                            if result.num_rows == 0
                                say_to_chan("#{$sender}: That ticket does not exist or it has been closed.")
                            else
                                result.each_hash do |h|
                                player=h['name'].gsub(/[\n\r]+/, " ")
                                message=h['message'].gsub(/[\n\r]+/, " ")
                                #say_to_chan("Ticket:'#{id}'")
                                #say_to_chan("Ticket: #{id} | Player: #{player} | Message: #{message}")
                                ticket_message = "Ticket: #{id} | Player: #{player} | Message: #{message}"
                                #say "PRIVMSG #{$sender} #{ticket_message}"
                                tickets.push(ticket_message)
                                end
                                con.close
                                say_to_chan(tickets)
                            end
                        end
                    end
                end
                if content.match('\A#comment')
                    say_to_chan("Commenting Soon to come")
                    string = content.scan(/!comment (.*)/)
                    say_to_chan(string)         
                end     
                if content.match('#die_bot')
                    if $sender == $master
                        say "QUIT"
                    else
                        say_to_chan("#{$sender}: You are not master! I do not have to obey you!")
                    end
                end     
                if content.match('#changenick')
                    #say_to_chan(':( ok cya')
                    if $sender == $master
                        nick = content.split(' ')[1]
                        say "NICK #{nick}"
                        $nick = nick
                    else
                        say_to_chan("#{$sender}: You are not master! I do not have to obey you!")
                    end
                end     
                if content.match('#help')
                    say_to_chan("[HELP]: [Heihachi's] IRC Bot.")
                    say_to_chan('[COMMANDS]: #help, #tickets, #online, #viewticket, #staff')
                    say_to_chan('More will be added in time')
                end              
            end
        end
    end
    def quit
        Thread.kill(loop)
        say "PART #{$channel} :cya guys :P"
        say 'QUIT'
    end
end

bot = SimpleIrcBot.new('#{$server}', '#{$channel}')

trap("INT"){ bot.quit }

bot.run
