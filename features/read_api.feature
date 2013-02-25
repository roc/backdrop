Feature: the performance platform read api

    Scenario: getting all the data in a bucket
        Given "licensing.json" is in "foo" bucket
         when I go to "/foo"
         then I should get back a status of "200"
          and the JSON should have "4" result(s)

    Scenario: my data does not have timestamps
        Given "dinosaurs.json" is in "rawr" bucket
         when I go to "/rawr"
         then I should get back a status of "200"
         and the JSON should have "4" result(s)

    Scenario: querying for data ON or AFTER a certain point
        Given "licensing.json" is in "foo" bucket
         when I go to "/foo?start_at=2012-12-13T01:01:01%2B00:00"
         then I should get back a status of "200"
          and the JSON should have "2" result(s)
          and the "1st" result should be "{"2012-12-14T01:01:01+00:00":{"licence_name": "Temporary events notice", "interaction": "success", "authority": "Westminster", "type": "success", "_id": "1237"}}"

    Scenario: querying for data BEFORE a certain point
        Given "licensing.json" is in "foo" bucket
         when I go to "/foo?end_at=2012-12-12T01:01:02%2B00:00"
         then I should get back a status of "200"
          and the JSON should have "2" result(s)
          and the "1st" result should be "{"2012-12-12T01:01:01+00:00":{"licence_name": "Temporary events notice", "interaction": "success", "authority": "Westminster", "type": "success", "_id": "1234"}}"

    Scenario: querying for data between two points
        Given "licensing.json" is in "foo" bucket
         when I go to "/foo?start_at=2012-12-12T01:01:02%2B00:00&end_at=2012-12-14T00:00:00%2B00:00"
         then I should get back a status of "200"
          and the JSON should have "1" result(s)
          and the "1st" result should be "{"2012-12-13T01:01:01+00:00":{"licence_name": "Temporary events notice", "interaction": "success", "authority": "Westminster", "type": "success", "_id": "1236"}}"


    Scenario: filtering by a key and value
        Given "licensing.json" is in "foo" bucket
         when I go to "/foo?filter_by=authority:Camden"
         then I should get back a status of "200"
          and the JSON should have "1" result(s)

    Scenario: grouping data by a key
        Given "licensing.json" is in "foo" bucket
         when I go to "/foo?group_by=authority"
         then I should get back a status of "200"
          and the JSON should have "2" result(s)
          and the "1st" result should be "{"Westminster": 3}"
          and the "2nd" result should be "{"Camden": 1}"

    Scenario: extracting data for a representation
        Given "licensing_2.json" is in "foo" bucket
         when I go to "/foo?group_by=authority&filter_by=licence_name:Temporary%20events%20notice"
         then I should get back a status of "200"
          and the JSON should have "2" result(s)
          and the "1st" result should be "{"Westminster": 3}"

        Given "licensing_2.json" is in "foo" bucket
         when I go to "/foo?group_by=licence_name&filter_by=authority:Westminster"
         then I should get back a status of "200"
          and the JSON should have "2" result(s)
          and the "1st" result should be "{"Temporary events notice": 3}"
          and the "2nd" result should be "{"Cat herding licence": 1}"

