#!/home/jamez/ruby/bin/ruby
require 'socket'
#require 'serverinfo.rb'
require 'rubygems'
require 'mysql'
require 'whenever'

#######################################################################################################
 
# File Needs to be named anything with a .rb after it.
if File.exists?("serverinfo_2.rb")
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
   eval File.open('serverinfo_2.rb').read
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
	sleep(5)
	say "PART #{$part}"
        sleep(4)
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
    def checks(switch)
        main = switch
        loop = Thread.new do
            while true
                new = Mysql.new('localhost', $user, $pass, 'characters')
                result = new.query("SELECT `ticketId`, `closedBy`, `name` from `characters`.`gm_tickets` WHERE `ticketId` in (SELECT MAX(`ticketId`) FROM `characters`.`gm_tickets`);")
                result.each_hash do |n|
                #say_to_chan(n['ticketId'])
                    if $last_ticket < n['ticketId']
                        if n['closedBy'] == '0'
                            say_to_chan("New unanswered ticket: #{n['ticketId']} Created by: #{n['name']}")
                        end
                    end
                    $last_ticket = n['ticketId']
                end
                regex = /(\$last_ticket.+)/
                replacement = "$last_ticket = '#{$last_ticket}'"
                "serverinfo_2.rb".each do |file_name|
                    text = File.read(file_name)
                    replace = text.gsub!(regex, replacement)
                    File.open(file_name, "w") { |file| file.puts replace }
                end
                say "PONG #{$~[1]}"
                sleep(100)
                say "PONG #{$~[1]}"
                sleep(100)
                say "PONG #{$~[1]}"
                sleep(100)
                say "PONG #{$~[1]}"
            end
        end
        if main == 1
            say_to_chan("Now checking for new tickets.")
            loop.join
        end
    end
    def send(t, m)
        sendraw "PRIVMSG #{t} :#{m}"
    end  
    def run
        until @socket.eof? do
            my_file = File.new("log.log", "w")
            $msg = @socket.gets
            puts $msg
            chan_1 = $msg.match(/PRIVMSG #{$channel} :(.*)S/)
            open('log.log', 'a') { |f| f.puts "#{chan_1}" }
        	#logging = my_file.puts "#{$msg}"
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
            if $msg.match(/^PING :(.*)$/)
                    say "PONG #{$~[1]}"
                    next
            end

            if $msg.match(/PRIVMSG #{$channel} :(.*)$/) || $msg.match(/PRIVMSG #{$nick} :(.*)$/)
                content = $~[1]
                words = $msg.split(" ")
                $sender = $msg.scan(/\A:(.*?)\!/)
                $sender = $sender.map(&:inspect).join(", ").tr('["]', '')
        
                #put matchers here            
                if content.match('#check')
                    s = content
                    yum = s.split(' ')[1]
                    if yum == "on"
                        checks(1)
                    elsif yum == "off"
                        checks(0)
                    end
                    say_to_chan(yum)
                end
            end
        end
    end
    def quit
        Thread.kill(loop)
        say 'QUIT'
    end
end

bot = SimpleIrcBot.new('#{$server}', '#{$channel}')

trap("INT"){ bot.quit }

bot.run
