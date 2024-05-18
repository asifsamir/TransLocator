from copy import deepcopy

from SearchAspects.CE_Scorer import CrossEncoderScorer
from Utils import JavaSourceParser


def get_methods_from_source_code(source_code):
    parser = JavaSourceParser(source_code)

    methods = parser.parse_methods()

    return methods


def score_by_cross_encoder(query, search_results, ce_model_path=None):

    ce_scorer = CrossEncoderScorer(ce_model_path)
    # iterate over the search results and get the source code
    for search_result in search_results:
        source_code = search_result["source_code"]

        # get methods from the source code
        methods = get_methods_from_source_code(source_code)

        # check if there are any methods in the source code. if not, max_score is 0
        if len(methods) == 0:
            search_result["score_ce"] = 0
            continue
        else:
            methods_2 = deepcopy(methods)

            # now, iterate over the methods and get the cross encoder score. Add the score to the methods dictionary replacing the method body
            for method_name, method_body in methods.items():
                score = ce_scorer.score(method_body, query)
                methods_2[method_name] = score

            # clear the methods from memory
            methods.clear()

            # find the max score and in search_result, add the max score as 'score_ce'
            max_score = max(methods_2.values())

            search_result["score_ce"] = max_score

    return search_results


if __name__ == '__main__':
    source_code = """/**
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package org.apache.camel.builder.xml;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;
import java.util.Set;

import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.Result;
import javax.xml.transform.Source;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerConfigurationException;
import javax.xml.transform.stream.StreamSource;

import org.apache.camel.Exchange;
import org.apache.camel.ExpectedBodyTypeException;
import org.apache.camel.Message;
import org.apache.camel.Processor;
import org.apache.camel.RuntimeTransformException;
import org.apache.camel.converter.jaxp.XmlConverter;

import static org.apache.camel.util.ObjectHelper.notNull;

/**
 * Creates a <a href="http://activemq.apache.org/camel/processor.html">Processor</a>
 * which performs an XSLT transformation of the IN message body
 * 
 * @version $Revision: 531854 $
 */
public class XsltBuilder implements Processor {
    private Map<String, Object> parameters = new HashMap<String, Object>();
    private XmlConverter converter = new XmlConverter();
    private Transformer transformer;
    private ResultHandlerFactory resultHandlerFactory = new StringResultHandlerFactory();
    private boolean failOnNullBody = true;

    public XsltBuilder() {
    }

    public XsltBuilder(Transformer transformer) {
        this.transformer = transformer;
    }

    @Override
    public String toString() {
        return "XSLT[" + transformer + "]";
    }

    public synchronized void process(Exchange exchange) throws Exception {
        Transformer transformer = getTransformer();
        if (transformer == null) {
            throw new IllegalArgumentException("No transformer configured!");
        }
        configureTransformer(transformer, exchange);
        Source source = getSource(exchange);
        ResultHandler resultHandler = resultHandlerFactory.createResult();
        Result result = resultHandler.getResult();
        transformer.transform(source, result);
        resultHandler.setBody(exchange.getIn());
    }

    // Builder methods
    // -------------------------------------------------------------------------

    /**
     * Creates an XSLT processor using the given transformer instance
     */
    public static XsltBuilder xslt(Transformer transformer) {
        return new XsltBuilder(transformer);
    }

    /**
     * Creates an XSLT processor using the given XSLT source
     */
    public static XsltBuilder xslt(Source xslt) throws TransformerConfigurationException {
        notNull(xslt, "xslt");
        XsltBuilder answer = new XsltBuilder();
        answer.setTransformerSource(xslt);
        return answer;
    }

    /**
     * Creates an XSLT processor using the given XSLT source
     */
    public static XsltBuilder xslt(File xslt) throws TransformerConfigurationException {
        notNull(xslt, "xslt");
        return xslt(new StreamSource(xslt));
    }

    /**
     * Creates an XSLT processor using the given XSLT source
     */
    public static XsltBuilder xslt(URL xslt) throws TransformerConfigurationException, IOException {
        notNull(xslt, "xslt");
        return xslt(xslt.openStream());
    }

    /**
     * Creates an XSLT processor using the given XSLT source
     */
    public static XsltBuilder xslt(InputStream xslt) throws TransformerConfigurationException, IOException {
        notNull(xslt, "xslt");
        return xslt(new StreamSource(xslt));
    }

    /**
     * Sets the output as being a byte[]
     */
    public XsltBuilder outputBytes() {
        setResultHandlerFactory(new StreamResultHandlerFactory());
        return this;
    }

    /**
     * Sets the output as being a String
     */
    public XsltBuilder outputString() {
        setResultHandlerFactory(new StringResultHandlerFactory());
        return this;
    }

    /**
     * Sets the output as being a DOM
     */
    public XsltBuilder outputDOM() {
        setResultHandlerFactory(new DomResultHandlerFactory());
        return this;
    }

    public XsltBuilder parameter(String name, Object value) {
        parameters.put(name, value);
        return this;
    }

    // Properties
    // -------------------------------------------------------------------------

    public Map<String, Object> getParameters() {
        return parameters;
    }

    public void setParameters(Map<String, Object> parameters) {
        this.parameters = parameters;
    }

    public Transformer getTransformer() {
        return transformer;
    }

    public void setTransformer(Transformer transformer) {
        this.transformer = transformer;
    }

    public boolean isFailOnNullBody() {
        return failOnNullBody;
    }

    public void setFailOnNullBody(boolean failOnNullBody) {
        this.failOnNullBody = failOnNullBody;
    }

    public ResultHandlerFactory getResultHandlerFactory() {
        return resultHandlerFactory;
    }

    public void setResultHandlerFactory(ResultHandlerFactory resultHandlerFactory) {
        this.resultHandlerFactory = resultHandlerFactory;
    }

    public void setTransformerSource(Source source) throws TransformerConfigurationException {
        setTransformer(converter.getTransformerFactory().newTransformer(source));
    }

    // Implementation methods
    // -------------------------------------------------------------------------

    /**
     * Converts the inbound body to a {@link Source}
     */
    protected Source getSource(Exchange exchange) {
        Message in = exchange.getIn();
        Source source = in.getBody(Source.class);
        if (source == null) {
            if (isFailOnNullBody()) {
                throw new ExpectedBodyTypeException(exchange, Source.class);
            } else {
                try {
                    source = converter.toSource(converter.createDocument());
                } catch (ParserConfigurationException e) {
                    throw new RuntimeTransformException(e);
                }
            }
        }
        return source;
    }

    /**
     * Configures the transformerwith exchange specific parameters
     */
    protected void configureTransformer(Transformer transformer, Exchange exchange) {
        transformer.clearParameters();

        addParameters(transformer, exchange.getProperties());
        addParameters(transformer, exchange.getIn().getHeaders());
        addParameters(transformer, getParameters());

        transformer.setParameter("exchange", exchange);
        transformer.setParameter("in", exchange.getIn());
        transformer.setParameter("out", exchange.getOut());
    }

    protected void addParameters(Transformer transformer, Map<String, Object> map) {
        Set<Map.Entry<String, Object>> propertyEntries = map.entrySet();
        for (Map.Entry<String, Object> entry : propertyEntries) {
            transformer.setParameter(entry.getKey(), entry.getValue());
        }
    }
}
"""
    query = '''From version 1.5 and onwards the CachingConnectionFactory will not allow any connections to be created once the application context has been closed. This is implemented by closing the connection factory as soon as closing of the application context is initiated (when the ContextClosedEvent is fired).
    This is quite abrupt and causes problems for code that may want to process requests and publish messages while the application context is still in it&apos;s closing stage.
    As an example we use spring-integration AMQP components (AmqpInboundChannelAdapter) for consuming inbound messages and these components implement the Spring SmartLifeCycle. This means that message consumers are not stopped until you reach the life-cycle processing stage in the application context closing (which happens after the ContextClosedEvent is fired). This causes problems as you cannot easily prevent incoming messages from arriving but you cannot send any outbound messages (since the connection factory is already closed). 
    For us this is major issue since it now limits our possibility to perform a graceful shutdown of our application, which worked well with prior versions.
    If closing is really required then I think it could make sense to defer it to a later stage by e.g. implementing Spring SmartLifeCycle and use the stop() method. Combined with a configurable phase that would give us the possibility to co-ordinate the closing with other components that should be stopped before we let the application context start destroying beans.'''
    search_results = [{'source_code': source_code}]
    search_results = score_by_cross_encoder(query, search_results, ce_model_path='F:\Models\Cross_encoder\CodeBert_Full_DS_Timed')
    # methods = get_methods_from_source_code(source_code)

    print(search_results)