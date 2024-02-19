module Jekyll
    module RegexMatch
        def regex_match(input_str, regex_str)
            regex = Regexp.new(regex_str)
            input_str.scan(regex).flatten
        end
  
      def regex_match_once(input_str, regex_str)
        regex = Regexp.new(regex_str)
        match = input_str.match(regex)
        return match.nil? ? nil : match[0]
      end
    end
  end
  
  Liquid::Template.register_filter(Jekyll::RegexMatch)